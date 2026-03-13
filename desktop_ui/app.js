const views = document.querySelectorAll('.view');
document.querySelectorAll('[data-view]').forEach((btn) => {
  btn.addEventListener('click', () => {
    views.forEach((v) => v.classList.remove('active'));
    document.getElementById(btn.dataset.view).classList.add('active');
  });
});

async function loadCustomers() {
  const data = await (await fetch('/api/customers')).json();
  const body = document.getElementById('customers-body');
  body.innerHTML = data.map((c) => `<tr><td>${c.customer_code}</td><td>${c.legal_name}</td><td>${c.email ?? ''}</td><td>${c.pending_amount.toFixed(2)} €</td></tr>`).join('');
}

async function loadProducts() {
  const data = await (await fetch('/api/products')).json();
  const body = document.getElementById('products-body');
  body.innerHTML = data.map((p) => `<tr><td>${p.sku}</td><td>${p.name}</td><td>${p.unit}</td><td>${Number(p.base_price).toFixed(2)} €</td></tr>`).join('');
}

document.getElementById('customer-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const payload = Object.fromEntries(fd.entries());
  const res = await fetch('/api/customers', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (!res.ok) {
    alert((await res.json()).error || 'Error al guardar cliente');
    return;
  }
  e.target.reset();
  await loadCustomers();
});

document.getElementById('product-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const payload = Object.fromEntries(fd.entries());
  payload.base_price = Number(payload.base_price);
  payload.default_vat_rate_id = 101;
  const res = await fetch('/api/products', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (!res.ok) {
    alert((await res.json()).error || 'Error al guardar producto');
    return;
  }
  e.target.reset();
  await loadProducts();
});

Promise.all([loadCustomers(), loadProducts()]);
