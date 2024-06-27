import { useRouter } from 'next/router';
import Link from 'next/link';
import Image from 'next/image';
import logo from '/public/llmproxyTransparent.png';
import { useAuth } from '../context/authContext'; // Adjust the path as needed

export default function Sidebar() {
  const router = useRouter();
  const { isAuthenticated, logout } = useAuth();
  const currentPath = router.pathname;

  return (
    <div className="w-64 bg-white p-4 flex flex-col items-start border-r-2">
      <div className="w-full flex justify-center mb-6">
        <Image src={logo} alt="Logo" className="w-28 h-28" />
      </div>
      <div className="font-semibold p-4 text-gray-400">MENU</div>
      <div className="flex flex-col justify-between space-y-2 w-full h-full">
        <div>
          <Link href="/myai" passHref>
            <button
              className={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
                currentPath === '/myai'
                  ? 'bg-blue-100 text-blue-800'
                  : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
              }`}
              type="button"
            >
              <i className="icon-key"></i>
              <span className="font-semibold">MyAI</span>
            </button>
          </Link>
          <Link href="/secrets" passHref>
            <button
              className={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
                currentPath === '/secrets'
                  ? 'bg-blue-100 text-blue-800'
                  : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
              }`}
              type="button"
            >
              <i className="icon-key"></i>
              <span className="font-semibold">Secrets</span>
            </button>
          </Link>
          <Link href="/analytics" passHref>
            <button
              className={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
                currentPath === '/analytics'
                  ? 'bg-blue-100 text-blue-800'
                  : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
              }`}
              type="button"
            >
              <i className="icon-analytics"></i>
              <span className="font-semibold">Analytics</span>
            </button>
          </Link>
          <Link href="/billing" passHref>
            <button
              className={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
                currentPath === '/billing'
                  ? 'bg-blue-100 text-blue-800'
                  : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
              }`}
              type="button"
            >
              <i className="icon-billing"></i>
              <span className="font-semibold">Billing</span>
            </button>
          </Link>
        </div>
        <div className="pb-8 pt-8 border-t-2">
          <Link href="/account" passHref>
            <button
              className={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
                currentPath === '/account'
                  ? 'bg-blue-100 text-blue-800'
                  : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
              }`}
              type="button"
            >
              <i className="icon-account"></i>
              <span className="font-semibold">Account</span>
            </button>
          </Link>
          <Link href="/settings" passHref>
            <button
              className={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
                currentPath === '/settings'
                  ? 'bg-blue-100 text-blue-800'
                  : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
              }`}
              type="button"
            >
              <i className="icon-settings"></i>
              <span className="font-semibold">Settings</span>
            </button>
          </Link>
          <button
            className="menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition text-gray-500 hover:bg-gray-200 hover:text-gray-700"
            type="button"
            onClick={logout}
          >
            <i className="icon-settings"></i>
            <span className="font-semibold">Logout</span>
          </button>
        </div>
      </div>
    </div>
  );
}
