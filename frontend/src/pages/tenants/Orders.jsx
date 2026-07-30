import { useCallback, useState } from "react";
import { Search, Eye } from "lucide-react";

import { fetchOrders } from "../../api/mailApi";
import usePolling from "../../hooks/usePolling";
import OrderDetailsModal from "../../components/OrderDetailsModal";

import "../../assets/css/TablePages.css";

export default function Orders() {
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");

  const [selectedOrder, setSelectedOrder] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const getData = useCallback(() => fetchOrders(), []);

  const {
    data: orders,
    loading,
    refresh,
  } = usePolling(getData, 5000);

  if (loading || !orders)
    return <div className="loading">Loading...</div>;

  const statuses = [
    "All",
    ...new Set(orders.map((o) => o.status)),
  ];

  const q = search.toLowerCase();

  const filtered = orders
    .filter((o) => filter === "All" || o.status === filter)
    .filter(
      (o) =>
        !q ||
        o.order_id?.toLowerCase().includes(q) ||
        o.customer_name?.toLowerCase().includes(q) ||
        o.customer_email?.toLowerCase().includes(q) ||
        o.product_name?.toLowerCase().includes(q) ||
        o.tracking_number?.toLowerCase().includes(q)
    );

  return (
    <>
      <div className="page-content">
        <div className="page-header">
          <h2>Orders</h2>
          <p>Track and manage all customer orders</p>
        </div>

        <div className="search-bar">
          <Search size={16} />

          <input
            type="text"
            placeholder="Search..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />
        </div>

        <div className="filter-bar">
          {statuses.map((s) => (
            <button
              key={s}
              className={`filter-btn ${
                filter === s ? "active" : ""
              }`}
              onClick={() => setFilter(s)}
            >
              {s}
            </button>
          ))}
        </div>

        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Product</th>
                <th>Status</th>
                <th>Date</th>
                <th>Tracking</th>
                <th>Payment</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map((o) => (
                <tr key={o.order_id}>
                  <td className="mono">
                    {o.order_id}
                  </td>

                  <td>
                    <div>{o.customer_name}</div>

                    <div className="sub-text">
                      {o.customer_email}
                    </div>
                  </td>

                  <td>{o.product_name}</td>

                  <td>
                    <span
                      className={`badge badge-${o.status
                        .toLowerCase()
                        .replace(/\s/g, "-")}`}
                    >
                      {o.status}
                    </span>
                  </td>

                  <td>{o.order_date}</td>

                  <td className="mono">
                    {o.tracking_number || "-"}
                  </td>

                  <td>
                    <span
                      className={`badge badge-${(
                        o.payment_status ||
                        "unknown"
                      ).toLowerCase()}`}
                    >
                      {o.payment_status || "N/A"}
                    </span>
                  </td>

                  <td>
                    <button
                      className="action-btn"
                      onClick={() => {
                        setSelectedOrder(
                          o.order_id
                        );
                        setShowModal(true);
                      }}
                    >
                      <Eye size={16} />
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <OrderDetailsModal
        open={showModal}
        orderId={selectedOrder}
        onClose={() => setShowModal(false)}
        onUpdated={() => refresh()}
      />
    </>
  );
}