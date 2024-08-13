<script lang="ts">
  import { DateTime } from 'luxon';
  import { Label } from "$lib/components/ui/label/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";

  let accountInfo = {
    firstName: '',
    lastName: '',
    email: '',
    username: localStorage.getItem('username') || ''
  };

  let passwordInfo = {
    currentPassword: '',
    newPassword: '',
    confirmNewPassword: ''
  };

  function saveAccountSettings() {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');
    toast.success(`Account information saved.`, {
      description: `${formatted_date}`,
    })
  }

  function changePassword() {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');
    toast.success(`Password has been changed.`, {
      description: `${formatted_date}`,
    })
  }
</script>

<div class="flex flex-col h-screen">
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Account</h1>
  <div class="flex-1 overflow-auto">
    <div class="m-10 border rounded-lg bg-white shadow">
      <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
      <div class="p-10 px-20 space-y-8">
        <div>
          <h3 class="text-xl font-semibold mb-4">Account Information</h3>
          <form on:submit|preventDefault={saveAccountSettings} class="space-y-4">
            <div class="flex space-x-4">
              <div class="w-1/2">
                <Label for="firstName" class="block text-gray-700">First Name</Label>
                <Input id="firstName" type="firstName" bind:value={accountInfo.firstName} class="mt-2" />
              </div>
              <div class="w-1/2">
                <Label for="lastName" class="block text-gray-700">Last Name</Label>
                <Input id="lastName" type="lastName" bind:value={accountInfo.lastName} class="mt-2"  />
              </div>
            </div>
            <div>
              <Label for="username" class="block text-gray-700">Username</Label>
              <Input disabled id="username" type="username" bind:value={accountInfo.username} class="mt-2" />
            </div>
            <div>
              <Label for="email" class="block text-gray-700">Email Address</Label>
              <Input id="email" type="email" bind:value={accountInfo.email} class="mt-2" />
            </div>
            <div class="pt-2">
              <Button type="submit" class="px-4 py-2 bg-blue-800 transition text-white rounded-lg hover:bg-blue-700 hover:transition focus:outline-none">Save Account Settings</Button>
            </div>
          </form>
        </div>
        
        <div class="pt-2">
          <h3 class="text-xl font-semibold mb-4">Change Password</h3>
          <form on:submit|preventDefault={changePassword} class="space-y-4">
            <div>
              <Label for="currentPassword" class="block text-gray-700">Current Password</Label>
              <Input id="currentPassword" type="currentPassword" bind:value={passwordInfo.currentPassword} class="mt-2" />
            </div>
            <div>
              <Label for="newPassword" class="block text-gray-700">New Password</Label>
              <Input id="newPassword" type="newPassword" bind:value={passwordInfo.newPassword} class="mt-2" />
            </div>
            <div>
              <Label for="confirmNewPassword" class="block text-gray-700">Confirm New Password</Label>
              <Input id="confirmNewPassword" type="confirmNewPassword" bind:value={passwordInfo.confirmNewPassword} class="mt-2" />
            </div>
            <div class="pt-2">
              <Button type="submit" class="px-4 py-2 bg-blue-800 transition text-white rounded-lg hover:bg-blue-700 hover:transition focus:outline-none">Change Password</Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
