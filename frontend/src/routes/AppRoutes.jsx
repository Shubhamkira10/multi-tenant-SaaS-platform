import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import PlatformLogin from "../pages/auth/PlatformLogin";
import TenantLogin from "../pages/auth/TenantLogin";

import PlatformDashboard from "../pages/dashboard/PlatformDashboard";
import TenantDashboard from "../pages/dashboard/TenantDashboard";

import Tenants from "../pages/tenants/Tenants";
import Agents from "../pages/agents/Agents";

import ProtectedRoute from "../components/ProtectedRoute";

import AssignTenantFeatures from "../pages/rbac/AssignTenantFeatures";

import Dashboard from "../pages/tenants/Dashboard";
import Orders from "../pages/tenants/Orders";
import Tickets from "../pages/tenants/Tickets";
import Customers from "../pages/tenants/Customers";
import Emails from "../pages/tenants/Emails";
import Conversations from "../pages/tenants/Conversations";
import Products from "../pages/tenants/Products";
import TestEmail from "../pages/tenants/TestEmail";
import TenantLayout from "../layouts/TenantLayout";
function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>

                {/* Authentication */}

                <Route path="/" element={<Navigate to="/login" />} />

                <Route path="/login" element={<PlatformLogin />} />

                <Route path="/tenant/login" element={<TenantLogin />} />

                {/* Platform */}

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <PlatformDashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenants"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <Tenants />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/agents"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <Agents />
                        </ProtectedRoute>
                    }
                />

                {/* Tenant */}

                <Route
                    path="/tenant"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <TenantLayout />
                        </ProtectedRoute>
                    }
                >
                    <Route index element={<TenantDashboard />} />
                    <Route path="dashboard" element={<TenantDashboard />} />
                    <Route path="overview" element={<Dashboard />} />
                    <Route path="orders" element={<Orders />} />
                    <Route path="tickets" element={<Tickets />} />
                    <Route path="customers" element={<Customers />} />
                    <Route path="mail-logs" element={<Emails />} />
                    <Route path="conversations" element={<Conversations />} />
                    <Route path="products" element={<Products />} />
                    <Route path="test-mail" element={<TestEmail />} />
                </Route>

                {/* 404 */}

                <Route
                    path="*"
                    element={<h2 className="text-center mt-5">404 Page Not Found</h2>}
                />

                <Route
                    path="/assign-features"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <AssignTenantFeatures />
                        </ProtectedRoute>
                    }
                />

            </Routes>
        </BrowserRouter>
    );
}

export default AppRoutes;