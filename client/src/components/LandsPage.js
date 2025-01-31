import React, { useEffect, useState } from 'react';

const LandsPage = () => {
    const [lands, setLands] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5555/lands")
            .then(res => res.json())
            .then(data => setLands(data));
    }, []);

    return (
        <div>
            <h1>Lands</h1>
            <ul>
                {lands.map(land => (
                    <li key={land.id}>
                        Location: {land.location} - Size: {land.size} sq.ft - Owner: {land.owner.name}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default LandsPage;
