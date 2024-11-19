import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useState } from "react";
import { Navigate } from "react-router-dom";
import Navbar from "/src/components/Navbar";
import Register from "/src/components/Register";
import Login from "/src/components/Login";
import Dashboard from "/src/components/Dashboard.jsx";

const App = () => {
  const [userId, setUserId] = useState(null);

  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Registration Page */}
        <Route path="/register" element={<Register />} />
        
        {/* Login Page */}
        <Route path="/login" element={<Login setUser={setUserId} />} />
        
        {/* Protected Dashboard Page */}
        <Route
          path="/dashboard"
          element={
            userId ? (
              <Dashboard userId={userId} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        {/* Default Route */}
        <Route path="*" element={<h1>Page Not Found</h1>} />
      </Routes>
    </Router>
  );
};

export default App;
