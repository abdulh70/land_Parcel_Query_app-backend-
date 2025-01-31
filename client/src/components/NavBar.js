import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/users">Users</Link></li>
                <li><Link to="/lands">Lands</Link></li>
                <li><Link to="/transactions">Transactions</Link></li>
            </ul>
        </nav>
    );
};

export default NavBar;
