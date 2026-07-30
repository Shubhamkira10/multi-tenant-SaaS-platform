const API_BASE = "http://localhost:8000/api";

/* -----------------------------
   Generic Request Helper
------------------------------*/

async function request(url, options = {}) {

  // Read JWT from localStorage
  const token = localStorage.getItem("access_token");

  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      "Content-Type": "application/json",

      // Attach JWT if available
      ...(token
        ? {
            Authorization: `Bearer ${token}`,
          }
        : {}),

      ...(options.headers || {}),
    },

    ...options,
  });

  if (!response.ok) {
    let error = "Request failed";

    try {
      const data = await response.json();
      error = data.detail || error;
    } catch (_) {}

    throw new Error(error);
  }

  if (response.status === 204) return null;

  const result = await response.json();

  if (
    result &&
    typeof result === "object" &&
    "data" in result
  ) {
    return result.data;
  }

  return result;
}
/* =============================
        DASHBOARD
=============================*/

export const fetchDashboard = () =>
  request("/mail/dashboard");

/* =============================
          ORDERS
=============================*/

export const fetchOrders = () =>
  request("/mail/orders");

export const fetchOrder = (orderId) =>
  request(`/mail/orders/${orderId}`);

export const updateOrder = (orderId, payload) =>
  request(`/mail/orders/${orderId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });

export const trackOrder = (orderId) =>
  request(`/mail/orders/${orderId}/track`, {
    method: "POST",
  });

export const returnOrder = (orderId) =>
  request(`/mail/orders/${orderId}/return`, {
    method: "POST",
  });

export const replaceOrder = (orderId) =>
  request(`/mail/orders/${orderId}/replacement`, {
    method: "POST",
  });

export const refundOrder = (orderId) =>
  request(`/mail/orders/${orderId}/refund`, {
    method: "POST",
  });

export const cancelOrder = (orderId) =>
  request(`/mail/orders/${orderId}/cancel`, {
    method: "POST",
  });

export const generateInvoice = (orderId) =>
  request(`/mail/orders/${orderId}/invoice`, {
    method: "POST",
  });

/* =============================
        CUSTOMERS
=============================*/

export const fetchCustomers = () =>
  request("/mail/customers");

export const fetchCustomer = (customerId) =>
  request(`/mail/customers/${customerId}`);

/* =============================
         PRODUCTS
=============================*/

export const fetchProducts = () =>
  request("/mail/products");

export const fetchProduct = (productId) =>
  request(`/mail/products/${productId}`);

/* =============================
          TICKETS
=============================*/

export const fetchTickets = () =>
  request("/mail/tickets");

export const createTicket = (payload) =>
  request("/mail/tickets", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/* =============================
      CONVERSATIONS
=============================*/

export const fetchConversations = () =>
  request("/mail/conversations");

export const sendMessage = (conversationId, payload) =>
  request(`/mail/conversations/${conversationId}/messages`, {
    method: "POST",
    body: JSON.stringify(payload),
  });

/* =============================
        EMAIL LOGS
=============================*/

export const fetchEmailLogs = () =>
  request("/mail/email-logs");

export const createEmailLog = (payload) =>
  request("/mail/email-logs", {
    method: "POST",
    body: JSON.stringify(payload),
  });



export const sendTestEmail = (payload) =>
  request("/mail/test-email", {
    method: "POST",
    body: JSON.stringify(payload),
  });

