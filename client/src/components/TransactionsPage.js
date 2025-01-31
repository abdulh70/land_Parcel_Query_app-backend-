// src/components/TransactionsPage.js
import React, { useState, useEffect } from 'react';

const TransactionsPage = () => {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5555/transactions')
            .then((res) => res.json())
            .then((data) => setTransactions(data));
    }, []);

    return (
        <div>
            <h1>Transactions</h1>
            <ul>
                {transactions.map((transaction) => (
                    <li key={transaction.transaction_id}>
                        Transaction ID: {transaction.transaction_id} - Buyer: {transaction.buyer.name} - Amount: ${transaction.amount}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TransactionsPage;
