import React, { useState, useEffect } from 'react';

const Notification: React.FC = () => {
  const [notifications, setNotifications] = useState<string[]>([]);

  useEffect(() => {
    // Example: Simulate loading notifications
    setNotifications(["New campaign added", "You have a new follower", "Reminder: Campaign ends soon!"]);
  }, []);

  return (
    <div className="notification-list">
      {notifications.length > 0 ? (
        <ul>
          {notifications.map((notification, index) => (
            <li key={index}>{notification}</li>
          ))}
        </ul>
      ) : (
        <p>No new notifications</p>
      )}
    </div>
  );
};

export default Notification;
