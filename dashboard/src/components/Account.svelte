<script lang="ts">
  import { DateTime } from 'luxon';
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";

  let firstName = '';
  let lastName = '';
  let email = '';
  let username = localStorage.getItem('username') || '';
  let currentPassword = '';
  let newPassword = '';
  let confirmNewPassword = '';

  function saveAccountSettings() {
    const current_date = DateTime.now().toISO();
    toast.success(`Account information saved.`, {
      description: `${current_date}`,
      action: {
        label: "Undo",
        onClick: () => console.info("Undo")
      }
    })
  }

  function changePassword() {
    const current_date = DateTime.now().toISO();
    toast.success(`Password has been changed.`, {
      description: `${current_date}`,
      action: {
        label: "Undo",
        onClick: () => console.info("Undo")
      }
    })
  }
</script>

<div class="flex flex-col flex-1">
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Account</h1>
  <div class="m-10 border rounded-lg bg-white shadow flex-1 overflow-auto">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
    <div class="p-10 px-20 space-y-8">
      <div>
        <h3 class="text-xl font-semibold mb-4">Account Information</h3>
        <form on:submit|preventDefault={saveAccountSettings} class="space-y-4">
          <div class="flex space-x-4">
            <div class="w-1/2">
              <div class="block text-gray-700">First Name</div>
              <input type="text" bind:value={firstName} class="form-input mt-1 block w-full border rounded p-2 bg-white" />
            </div>
            <div class="w-1/2">
              <div class="block text-gray-700">Last Name</div>
              <input type="text" bind:value={lastName} class="form-input mt-1 block w-full border rounded p-2 bg-white" />
            </div>
          </div>
          <div>
            <div class="block text-gray-700">Username</div>
            <input type="text" bind:value={username} class="form-input mt-1 block w-full border rounded p-2 bg-gray-200" readonly />
          </div>
          <div>
            <div class="block text-gray-700">Email Address</div>
            <input type="email" bind:value={email} class="form-input mt-1 block w-full border rounded p-2 bg-white" />
          </div>
          <div class="pt-2">
            <button type="submit" class="px-4 py-2 bg-blue-800 transition text-white rounded-lg hover:bg-blue-700 hover:transition focus:outline-none">Save Account Settings</button>
          </div>
        </form>
      </div>

      <div class="pt-2">
        <h3 class="text-xl font-semibold mb-4">Change Password</h3>
        <form on:submit|preventDefault={changePassword} class="space-y-4">
          <div>
            <div class="block text-gray-700">Current Password</div>
            <input type="password" bind:value={currentPassword} class="form-input mt-1 block w-full border rounded p-2 bg-white" />
          </div>
          <div>
            <div class="block text-gray-700">New Password</div>
            <input type="password" bind:value={newPassword} class="form-input mt-1 block w-full border rounded p-2 bg-white" />
          </div>
          <div>
            <div class="block text-gray-700">Confirm New Password</div>
            <input type="password" bind:value={confirmNewPassword} class="form-input mt-1 block w-full border rounded p-2 bg-white" />
          </div>
          <div class="pt-2">
            <button type="submit" class="px-4 py-2 bg-blue-800 transition text-white rounded-lg hover:bg-blue-700 hover:transition focus:outline-none">Change Password</button>
          </div>
        </form>
      </div>  
    </div>
  </div>
</div>
