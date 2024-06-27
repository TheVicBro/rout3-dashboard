import Link from 'next/link';

export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-gray-800 text-white flex flex-col">
      <nav className="flex-grow">
        <ul className="space-y-2 p-4">
          <li className="hover:bg-gray-700 p-2 rounded">
            <Link href="/myai" className="block">MyAI</Link>
          </li>
          <li className="hover:bg-gray-700 p-2 rounded">
            <Link href="/secrets" className="block">Secrets</Link>
          </li>
          <li className="hover:bg-gray-700 p-2 rounded">
            <Link href="/analytics" className="block">Analytics</Link>
          </li>
          <li className="hover:bg-gray-700 p-2 rounded">
            <Link href="/billing" className="block">Billing</Link>
          </li>
          <li className="hover:bg-gray-700 p-2 rounded">
            <Link href="/account" className="block">Account</Link>
          </li>
          <li className="hover:bg-gray-700 p-2 rounded">
            <Link href="/settings" className="block">Settings</Link>
          </li>
        </ul>
      </nav>
      <div className="p-4">
        <button className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">Logout</button>
      </div>
    </div>
  );
}
