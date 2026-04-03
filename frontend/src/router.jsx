import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import AdminDashboard from "./pages/AdminDashboard";
import UserDashboard from "./pages/UserDashboard";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Verify from "./pages/Verify";


function ProtectedRoute({

  children,
  roleRequired

}) {

  const token =
    localStorage.getItem("token");

  const role =
    localStorage.getItem("role");

  if (!token) {

    return <Navigate to="/login" />;

  }

  if (
    roleRequired &&
    role !== roleRequired
  ) {

    return <Navigate to="/user" />;

  }

  return children;

}


export default function Router() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Navigate to="/login" />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/verify"
          element={<Verify />}
        />

        <Route
          path="/admin"
          element={

            <ProtectedRoute roleRequired="admin">

              <AdminDashboard />

            </ProtectedRoute>

          }
        />

        <Route
          path="/user"
          element={

            <ProtectedRoute>

              <UserDashboard />

            </ProtectedRoute>

          }
        />

      </Routes>

    </BrowserRouter>

  );

}