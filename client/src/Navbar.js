import React from 'react';
import './Navbar.css';

const Navbar = ({ isSatellite, toggleSatellite, pointCount }) => { // Receive pointCount
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button
          onClick={toggleSatellite}
          className="satellite-toggle-button"
        >
          {isSatellite ? "Switch to Street Mode" : "Switch to Satellite Mode"}
        </button>
      </div>
      <div className="navbar-mid-left">
        <p>Number of Cameras: {pointCount}</p>
        {/* Display point count */}
      </div>
      <div className="navbar-center">
        <p>EYE IN THE SKY</p>
      </div>
      <div className="navbar-mid-right">
        <p>
          If prompted for credentials:
        </p>
      </div>
      <div className="navbar-right">
        <p>Username: admin</p>
        <p>Password: admin</p>
      </div>
    </nav>
  );
};

export default Navbar;