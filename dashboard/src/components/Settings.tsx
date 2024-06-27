import React, { useState } from 'react';

const Settings: React.FC = () => {
  const [enableNotifications, setEnableNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div className="flex flex-col flex-1">
      <h1 className="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Settings</h1>
      <div className="m-10 border rounded-lg bg-white shadow flex-1 overflow-auto">
        <h2 className="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
        <div className="p-20 px-64">
          <div>
            <h3 className="text-xl font-semibold mb-4">General Settings</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="text-gray-700">Enable Notifications</div>
                <label className="cursor-pointer relative inline-block w-14 h-8">
                  <input type="checkbox" checked={enableNotifications} onChange={(e) => setEnableNotifications(e.target.checked)} className="opacity-0 w-0 h-0" />
                  <span className={`absolute top-0 left-0 right-0 bottom-0 rounded-full transition duration-200 ease-in-out ${enableNotifications ? 'bg-blue-800' : 'bg-gray-400'}`}></span>
                  <span className={`absolute left-1 top-1 w-6 h-6 bg-white rounded-full transition transform duration-200 ease-in-out ${enableNotifications ? 'translate-x-6' : ''}`}></span>
                </label>
              </div>
              <div className="flex items-center justify-between">
                <div className="text-gray-700">Dark Mode</div>
                <label className="cursor-pointer relative inline-block w-14 h-8">
                  <input type="checkbox" checked={darkMode} onChange={(e) => setDarkMode(e.target.checked)} className="opacity-0 w-0 h-0" />
                  <span className={`absolute top-0 left-0 right-0 bottom-0 rounded-full transition duration-200 ease-in-out ${darkMode ? 'bg-blue-800' : 'bg-gray-400'}`}></span>
                  <span className={`absolute left-1 top-1 w-6 h-6 bg-white rounded-full transition transform duration-200 ease-in-out ${darkMode ? 'translate-x-6' : ''}`}></span>
                </label>
              </div>
            </div>
          </div>
          <div className="pt-6">
            <button className="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none">Save Changes</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
