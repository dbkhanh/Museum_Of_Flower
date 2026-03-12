/**
 * Shared basket functionality - icon, API calls, and view modal
 */
const BASKET_STORAGE_KEY = 'museum_basket_id';
const API_BASE = '';

function getBasketId() {
    return localStorage.getItem(BASKET_STORAGE_KEY);
}

function setBasketId(id) {
    localStorage.setItem(BASKET_STORAGE_KEY, id);
}

function updateBasketBadge() {
    const badge = document.getElementById('basket-count');
    const basketId = getBasketId();
    if (!badge) return;

    if (!basketId) {
        badge.textContent = '0';
        badge.style.display = 'none';
        return;
    }

    fetch(`${API_BASE}/baskets/${basketId}`)
        .then(res => res.ok ? res.json() : null)
        .then(basket => {
            if (basket && basket.total_tickets > 0) {
                badge.textContent = basket.total_tickets;
                badge.style.display = 'inline-flex';
            } else {
                badge.textContent = '0';
                badge.style.display = 'none';
            }
        })
        .catch(() => {
            badge.textContent = '0';
            badge.style.display = 'none';
        });
}

function showBasketModal() {
    const modal = document.getElementById('basket-modal');
    const content = document.getElementById('basket-modal-body');
    const basketId = getBasketId();

    if (!modal || !content) return;

    if (!basketId) {
        content.innerHTML = '<p class="text-muted mb-0">Your basket is empty. <a href="/static/tickets.html">Browse tickets</a> to add items.</p>';
        modal.style.display = 'flex';
        return;
    }

    content.innerHTML = '<p class="text-muted mb-0">Loading...</p>';
    modal.style.display = 'flex';

    Promise.all([
        fetch(`${API_BASE}/baskets/${basketId}`).then(r => {
            if (!r.ok) throw new Error(r.status === 404 ? 'BASKET_NOT_FOUND' : 'Failed to load basket');
            return r.json();
        }),
        fetch(`${API_BASE}/baskets/${basketId}/tickets`).then(r => {
            if (!r.ok) throw new Error(r.status === 404 ? 'BASKET_NOT_FOUND' : 'Failed to load tickets');
            return r.json();
        }),
        fetch(`${API_BASE}/baskets/${basketId}/purchases`).then(r => r.ok ? r.json() : [])
    ]).then(([basket, tickets, purchases]) => {
        if (!Array.isArray(tickets) || tickets.length === 0) {
            let html = '<p class="text-muted mb-3">Your basket is empty. <a href="/static/tickets.html">Browse tickets</a> to add items.</p>';
            if (Array.isArray(purchases) && purchases.length > 0) {
                html += '<h6 class="mt-4 mb-2">Previous Purchases</h6>';
                purchases.forEach(p => {
                    let items = {};
                    try { items = p.items_json ? JSON.parse(p.items_json) : {}; } catch (e) {}
                    const date = p.created_at ? new Date(p.created_at).toLocaleDateString() : '';
                    html += `<div class="border rounded p-2 mb-2 small">`;
                    html += `<div class="text-muted mb-1">${date}</div>`;
                    for (const [name, info] of Object.entries(items)) {
                        const subtotal = (info.count || 0) * (info.price || 0);
                        html += `<div class="d-flex justify-content-between"><span>${name} × ${info.count || 0}</span><span>$${subtotal.toFixed(2)}</span></div>`;
                    }
                    html += `<div class="d-flex justify-content-between fw-bold mt-1"><span>Total</span><span>$${parseFloat(p.total_amount || 0).toFixed(2)}</span></div>`;
                    html += `</div>`;
                });
            }
            content.innerHTML = html;
            return;
        }

        const ticketGroups = {};
        tickets.forEach(t => {
            const key = `${t.type} - ${t.subtype}`;
            if (!ticketGroups[key]) ticketGroups[key] = { count: 0, price: parseFloat(t.price), ticketIds: [] };
            ticketGroups[key].count++;
            ticketGroups[key].ticketIds.push(t.ticket_id);
        });

        let html = '<div class="basket-items">';
        let total = 0;
        for (const [name, info] of Object.entries(ticketGroups)) {
            const subtotal = info.count * info.price;
            total += subtotal;
            const removeBtn = info.count > 0 ? `<button type="button" class="btn btn-sm btn-outline-danger ml-2 remove-ticket" data-ticket-id="${info.ticketIds[0]}" title="Remove one">×</button>` : '';
            html += `<div class="d-flex justify-content-between align-items-center py-2 border-bottom basket-item-row">
                <span>${name} × ${info.count} ${removeBtn}</span>
                <span>$${subtotal.toFixed(2)}</span>
            </div>`;
        }
        html += `<div class="d-flex justify-content-between align-items-center py-3 mt-2 fw-bold">
            <span>Total (${basket.total_tickets} tickets)</span>
            <span>$${total.toFixed(2)}</span>
        </div>`;
        html += `<div class="mt-3">
            <a href="/static/checkout.html" class="btn btn-primary btn-block">Checkout</a>
        </div>`;
        if (Array.isArray(purchases) && purchases.length > 0) {
            html += '<h6 class="mt-4 mb-2">Previous Purchases</h6>';
            purchases.forEach(p => {
                let items = {};
                try { items = p.items_json ? JSON.parse(p.items_json) : {}; } catch (e) {}
                const date = p.created_at ? new Date(p.created_at).toLocaleDateString() : '';
                html += `<div class="border rounded p-2 mb-2 small">`;
                html += `<div class="text-muted mb-1">${date}</div>`;
                for (const [name, info] of Object.entries(items)) {
                    const subtotal = (info.count || 0) * (info.price || 0);
                    html += `<div class="d-flex justify-content-between"><span>${name} × ${info.count || 0}</span><span>$${subtotal.toFixed(2)}</span></div>`;
                }
                html += `<div class="d-flex justify-content-between fw-bold mt-1"><span>Total</span><span>$${parseFloat(p.total_amount || 0).toFixed(2)}</span></div>`;
                html += `</div>`;
            });
        }
        html += '</div>';
        content.innerHTML = html;

        content.querySelectorAll('.remove-ticket').forEach(btn => {
            btn.addEventListener('click', async function() {
                const ticketId = this.getAttribute('data-ticket-id');
                if (!ticketId) return;
                try {
                    const res = await fetch(`${API_BASE}/tickets/${ticketId}`, { method: 'DELETE' });
                    if (res.ok) {
                        showBasketModal();
                        updateBasketBadge();
                    }
                } catch (e) {}
            });
        });
    }).catch(err => {
        if (err.message === 'BASKET_NOT_FOUND') {
            localStorage.removeItem(BASKET_STORAGE_KEY);
            content.innerHTML = '<p class="text-muted mb-0">Your basket session expired or was cleared. <a href="/static/tickets.html">Add tickets</a> to create a new basket.</p>';
        } else {
            content.innerHTML = '<p class="text-danger mb-0">Unable to load basket. Please try again.</p>';
        }
    });
}

function closeBasketModal() {
    const modal = document.getElementById('basket-modal');
    if (modal) modal.style.display = 'none';
}

function initBasketIcon() {
    const basketIcon = document.getElementById('basket-icon');
    if (basketIcon) {
        basketIcon.addEventListener('click', (e) => {
            e.preventDefault();
            showBasketModal();
        });
    }
    const closeBtn = document.getElementById('basket-modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeBasketModal);
    }
    const modal = document.getElementById('basket-modal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeBasketModal();
        });
    }
    updateBasketBadge();
}

// Map form labels to API enum values
const SUBTYPE_MAP = {
    'Adults': 'Adult',
    'Children': 'Children',
    'Seniors': 'Senior',
    'Individual': 'Individual',
    'Family': 'Family'
};

const TICKET_TYPE_MAP = {
    'General Admission': 'General Admission',
    'Guided Tour': 'Guided Tour',
    'Annual Pass': 'Annual Pass'
};

function parsePrice(priceStr) {
    const match = String(priceStr).match(/\$?([\d.]+)/);
    return match ? parseFloat(match[1]) : 0;
}

/**
 * Add tickets to basket. items: array of { label, quantity, priceStr }
 * e.g. [{ label: 'Adults', quantity: 2, priceStr: '$20' }]
 */
async function addTicketsToBasket(ticketType, items) {
    let basketId = getBasketId();

    if (!basketId) {
        const createRes = await fetch(`${API_BASE}/baskets/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ total_tickets: 0 })
        });
        if (!createRes.ok) throw new Error('Failed to create basket');
        const basket = await createRes.json();
        basketId = basket.basket_id;
        setBasketId(basketId);
    }

    const ticketsToCreate = [];
    for (const item of items) {
        const q = parseInt(item.quantity, 10) || 0;
        if (q <= 0) continue;
        const subtype = SUBTYPE_MAP[item.label] || item.label;
        const price = parsePrice(item.priceStr || '0');
        for (let i = 0; i < q; i++) {
            ticketsToCreate.push({
                type: TICKET_TYPE_MAP[ticketType] || ticketType,
                subtype: subtype,
                price: price,
                basket_id: parseInt(basketId, 10)
            });
        }
    }

    for (const ticket of ticketsToCreate) {
        const res = await fetch(`${API_BASE}/tickets/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ticket)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || 'Failed to add ticket');
        }
    }

    updateBasketBadge();
    return basketId;
}
