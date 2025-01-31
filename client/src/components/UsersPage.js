// src/components/UsersPage.js
import React, { useState, useEffect } from 'react';

const UsersPage = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5555/users')
            .then((res) => res.json())
            .then((data) => setUsers(data));
    }, []);

    return (
        <div>
            <h1>Users</h1>
            <ul>
                {users.map((user) => (
                    <li key={user.id}>{user.name} - {user.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default UsersPage;
