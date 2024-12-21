import React, { useState, useEffect, useCallback } from 'react';

interface Notification {
  message: string;
  status: 'success' | 'error' | 'info';
}

const NotificationComponent: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const fetchData = useCallback(async (url: string) => {
    try {
      const response = await fetch(url);
      const data = await response.json();
      
      if (data.status === "error") {
        setNotifications((prev) => [...prev, { message: data.message, status: 'error' }]);
      } else {
        setNotifications((prev) => [...prev, { message: data.message, status: 'success' }]);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setNotifications((prev) => [...prev, { message: "Something went wrong.", status: 'error' }]);
    }
  }, []);

  useEffect(() => {
    fetchData('http://localhost:5000/search/charity?name=test');
  }, [fetchData]);

  return (
    <div className="notification-list">
      {notifications.length > 0 ? (
        <ul>
          {notifications.map((notification, index) => (
            <li key={index} className={notification.status}>
              {notification.message}
            </li>
          ))}
        </ul>
      ) : (
        <p>No new notifications</p>
      )}
    </div>
  );
};

export default NotificationComponent;
