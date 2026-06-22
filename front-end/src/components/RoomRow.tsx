import React from 'react';

interface RoomRowProps {
    name: string;
    capacity: string;
    status: string;
    action: string;
}

const RoomRow: React.FC<RoomRowProps> = ({ name, capacity, status, action }) => {
    const isLocked = status.toLowerCase() === 'locked';
    const isFull = action.toLowerCase() === 'full';

    return (
        <div className="table-row">
            <div className="column group-name">{name}</div>
            <div className={`column capacity ${isFull ? 'full-capacity' : ''}`}>{capacity}</div>
            <div className={`column status ${isLocked ? 'status-locked' : 'status-open'}`}>
                {status}
            </div>
            <div className="column action">
                <button
                    className={isFull ? 'btn-full' : 'btn-join'}
                    disabled={isFull}
                >
                    {action}
                </button>
            </div>
        </div>
    );
};

export default RoomRow;
