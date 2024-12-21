import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const performLogout = async () => {
            try {
                const response = await fetch('http://localhost:5000/auth/logout', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    localStorage.clear();
                    sessionStorage.clear();
                }
            } catch (error) {
                console.error('Logout error:', error);
            } finally {
                // Wait 0.5 seconds then redirect to home
                setTimeout(() => {
                    navigate('/auth');
                }, 500);
            }
        };

        performLogout();
    }, [navigate]);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="text-center">
                <h2 className="text-xl font-semibold mb-2">Logging out...</h2>
                <p className="text-gray-600">Please wait</p>
            </div>
        </div>
    );
};

export default Logout;