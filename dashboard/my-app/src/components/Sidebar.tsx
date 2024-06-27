import React from "react";
import Link from 'next/link';

export default function Sidebar() {
  return (
    <div className="w-64 bg-gray-800 text-white">
      <nav>
        <ul>
          <li><Link href="/myai">MyAI</Link></li>
          <li><Link href="/secrets">Secrets</Link></li>
          <li><Link href="/analytics">Analytics</Link></li>
          <li><Link href="/billing">Billing</Link></li>
          <li><Link href="/account">Account</Link></li>
          <li><Link href="/settings">Settings</Link></li>
        </ul>
      </nav>
    </div>
  );
}
