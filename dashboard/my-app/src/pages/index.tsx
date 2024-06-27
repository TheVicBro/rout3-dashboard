import React from "react";
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Secrets from '../components/Secrets';
// import Analytics from '../components/Analytics';
// import Billing from '../components/Billing';
// import Settings from '../components/Settings';
// import Account from '../components/Account';
import Login from '../components/Login';
// import MyAI from '../components/MyAI';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (localStorage.getItem("authToken")) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    router.push('/secrets');
  };

  return (
    <div>
      {isAuthenticated ? (
        <div className="flex h-screen bg-slate-100">
          <Sidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* {router.pathname === '/myai' && <MyAI />} */}
            {router.pathname === '/secrets' && <Secrets />}
            {/* {router.pathname === '/analytics' && <Analytics />}
            {router.pathname === '/billing' && <Billing />}
            {router.pathname === '/account' && <Account />}
            {router.pathname === '/settings' && <Settings />} */}
            {router.pathname === '/' && <Secrets />}
          </div>
        </div>
      ) : (
        <div className="min-h-screen flex items-center justify-center bg-slate-100">
          <Login onLoginSuccess={handleLoginSuccess} />
        </div>
      )}
    </div>
  );
}
