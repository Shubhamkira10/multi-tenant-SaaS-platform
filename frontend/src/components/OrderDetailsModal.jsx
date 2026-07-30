import { useEffect, useState } from "react";
import {
  fetchOrder,
  updateOrder,
  trackOrder,
  returnOrder,
  replaceOrder,
  refundOrder,
  cancelOrder,
  generateInvoice,
} from "../api/mailApi";

import "../assets/css/TablePages.css";

export default function OrderDetailsModal({
  orderId,
  open,
  onClose,
  onUpdated,
}) {
  const [order, setOrder] = useState(null);
  const [address, setAddress] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open || !orderId) return;

    loadOrder();
  }, [orderId, open]);

  async function loadOrder() {
    setLoading(true);

    try {
      const data = await fetchOrder(orderId);
      setOrder(data);
      setAddress(data.shipping_address || "");
    } catch (err) {
      alert(err.message);
    }

    setLoading(false);
  }

  async function saveAddress() {
    try {
      await updateOrder(order.order_id, {
        shipping_address: address,
      });

      alert("Address Updated");

      loadOrder();

      if (onUpdated) onUpdated();
    } catch (err) {
      alert(err.message);
    }
  }

  async function handleTrack() {
    const result = await trackOrder(order.order_id);
    alert(result.message || JSON.stringify(result));
  }

  async function handleReturn() {
    const result = await returnOrder(order.order_id);
    alert(result.message || "Return Request Created");

    if (onUpdated) onUpdated();
  }

  async function handleReplacement() {
    const result = await replaceOrder(order.order_id);
    alert(result.message || "Replacement Request Created");

    if (onUpdated) onUpdated();
  }

  async function handleRefund() {
    const result = await refundOrder(order.order_id);
    alert(result.message || "Refund Request Created");

    if (onUpdated) onUpdated();
  }

  async function handleCancel() {
    const result = await cancelOrder(order.order_id);
    alert(result.message || "Cancellation Request Created");

    if (onUpdated) onUpdated();
  }

  async function handleInvoice() {
    const result = await generateInvoice(order.order_id);

    alert(result.message || "Invoice Generated");
  }

  if (!open) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-card">

        {loading && <p>Loading...</p>}

        {!loading && order && (
          <>
            <div className="modal-header">
              <h2>{order.order_id}</h2>

              <button
                className="close-btn"
                onClick={onClose}
              >
                ✕
              </button>
            </div>

            <hr />

            <div className="detail-grid">

              <div>
                <strong>Customer</strong>
                <p>{order.customer_name}</p>
              </div>

              <div>
                <strong>Email</strong>
                <p>{order.customer_email}</p>
              </div>

              <div>
                <strong>Product</strong>
                <p>{order.product_name}</p>
              </div>

              <div>
                <strong>Status</strong>
                <p>{order.status}</p>
              </div>

              <div>
                <strong>Payment</strong>
                <p>{order.payment_status}</p>
              </div>

              <div>
                <strong>Tracking</strong>
                <p>{order.tracking_number || "-"}</p>
              </div>

            </div>

            <hr />

            <h3>Shipping Address</h3>

            <textarea
              rows="4"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
            />

            <button
              className="primary-btn"
              onClick={saveAddress}
            >
              Save Address
            </button>

            <hr />

            <div className="action-grid">

              <button onClick={handleTrack}>
                Track
              </button>

              <button onClick={handleReturn}>
                Return
              </button>

              <button onClick={handleReplacement}>
                Replacement
              </button>

              <button onClick={handleRefund}>
                Refund
              </button>

              <button onClick={handleCancel}>
                Cancel
              </button>

              <button onClick={handleInvoice}>
                GST Invoice
              </button>

            </div>

          </>
        )}

      </div>
    </div>
  );
}