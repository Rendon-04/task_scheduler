import React from "react";
import { Link, useNavigate } from "react-router-dom"
import "/src/components/Navbar.css"

export default function Navbar({ isLoggedIn, handleLogout }) {
    const navigate = useNavigate();
  
    const handleLogoutClick = () => {
      handleLogout(); // Call the logout function
      navigate("/login"); // Redirect to login after logout
    };
  
    return (
      <nav className="navbar">
        <ul className="navbar-menu">
          {!isLoggedIn && (
            <li className="navbar-item">
              <Link to="/login" className="navbar-link">
                Login
              </Link>
            </li>
          )}
          {isLoggedIn && (
            <li className="navbar-item">
              <button
                onClick={handleLogoutClick}
                className="navbar-link logout-btn"
              >
                Logout
              </button>
            </li>
          )}
          <li className="navbar-item">
            <Link to="/register" className="navbar-link">
              Register
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/dashboard" className="navbar-link">
              Dashboard
            </Link>
          </li>
        </ul>
      </nav>
    );
  }
  ;