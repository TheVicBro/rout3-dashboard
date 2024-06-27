import React, { useState } from 'react';

export default function Account() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');

  const saveAccountSettings = () => {
    console.log('Account settings saved');
  };

  const changePassword = () => {
    console.log('Password changed');
  };

  return (
    <div className="flex flex-col flex-1">
      <h1 className="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Account</h1>
      <div className="m-10 border rounded-lg bg-white shadow flex-1 overflow-auto">
        <h2 className="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
        <div className="p-10 px-20 space-y-8">
          <div>
            <h3 className="text-xl font-semibold mb-4">Account Information</h3>
            <form onSubmit={(e) => { e.preventDefault(); saveAccountSettings(); }} className="space-y-4">
              <div className="flex space-x-4">
                <div className="w-1/2">
                  <div className="block text-gray-700">First Name</div>
                  <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
                </div>
                <div className="w-1/2">
                  <div className="block text-gray-700">Last Name</div>
                  <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
                </div>
              </div>
              <div>
                <div className="block text-gray-700">Username</div>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
              </div>
              <div>
                <div className="block text-gray-700">Email Address</div>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
              </div>
              <div className="pt-2">
                <button type="submit" className="px-4 py-2 bg-blue-800 transition text-white rounded-lg hover:bg-blue-700 hover:transition focus:outline-none">Save Account Settings</button>
              </div>
            </form>
          </div>
          <div className="pt-2">
            <h3 className="text-xl font-semibold mb-4">Change Password</h3>
            <form onSubmit={(e) => { e.preventDefault(); changePassword(); }} className="space-y-4">
              <div>
                <div className="block text-gray-700">Current Password</div>
                <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
              </div>
              <div>
                <div className="block text-gray-700">New Password</div>
                <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
              </div>
              <div>
                <div className="block text-gray-700">Confirm New Password</div>
                <input type="password" value={confirmNewPassword} onChange={(e) => setConfirmNewPassword(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
              </div>
              <div className="pt-2">
                <button type="submit" className="px-4 py-2 bg-blue-800 transition text-white rounded-lg hover:bg-blue-700 hover:transition focus:outline-none">Change Password</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
