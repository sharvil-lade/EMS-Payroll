import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1><Link to="/">EMS & Payroll</Link></h1>
      <div className="nav-links">
        {/* <Link to="/">Dashboard</Link>
        <Link to="/employees">Employees</Link>
        <Link to="/attendance">Attendance</Link>
        <Link to="/payroll">Payroll</Link> */}
      </div>
    </nav>
  );
};

export default Navbar;
