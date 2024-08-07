<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { z } from "zod";
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button/index.js";
  import Logo from '/llmproxyTransparent.png';
  import { UserRound, Mail, Lock } from 'lucide-svelte';

  const dispatch = createEventDispatcher();

  const LoginSchema = z.object({
    usernameOrEmail: z.string().min(1, "Username or email is required"),
    password: z.string().min(6, "Password must be at least 6 characters"),
  });

  const RegisterSchema = z.object({
    username: z.string().min(1, "Username is required"),
    email: z.string().email("Invalid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string().min(1, "Confirm password is required")
  }).refine(data => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"]
  });

  type LoginForm = z.infer<typeof LoginSchema>;
  type RegisterForm = z.infer<typeof RegisterSchema>;

  let form: LoginForm & Partial<RegisterForm> = {
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    usernameOrEmail: "",
  };

  type FormErrors = Partial<Record<keyof (LoginForm & RegisterForm) | 'form', string[] | string>>;
  let errors: FormErrors = {};

  let showRegister = false;

  function registerLoginSwitch() {
    showRegister = !showRegister;
    resetForm();
  }

  function resetForm() {
    form = {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      usernameOrEmail: "",
    };
    errors = {};
  }

  async function login() {
    console.log("LOGIN REQUEST")
    errors = {};
    const result = LoginSchema.safeParse(form);

    if (!result.success) {
      errors = result.error.formErrors.fieldErrors;
      return;
    }

    const { usernameOrEmail, password } = result.data;
    const response = await fetch(`http://127.0.0.1:8000/api/v1/login/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ username: usernameOrEmail, password }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("authToken", data.access_token);
      dispatch("loginSuccess");
    } else {
      errors.form = "Login failed";
    }
  }

  async function register() {
    errors = {};
    const result = RegisterSchema.safeParse(form);

    if (!result.success) {
      errors = result.error.formErrors.fieldErrors;
      return;
    }

    const { username, email, password } = result.data;
    const response = await fetch(`http://127.0.0.1:8000/api/v1/user`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, password }),
    });

    if (response.ok) {
      alert("Registration successful");
      showRegister = false;
      form.usernameOrEmail = username;
      login();
    } else {
      errors.form = "Registration failed";
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      if (showRegister) {
        register();
      } else {
        login();
      }
    }
  }
</script>

<div class="flex items-center justify-center bg-gray-100">
  <div class="flex bg-white rounded-lg shadow-lg w-full max-w-4xl">
    <div class="flex flex-col p-12 pt-8 w-1/2 justify-center">
      <div class="flex justify-center mb-4">
        <img src={Logo} alt="Logo" class="w-2/5 object-cover object-center rounded-r-lg" />
      </div>
      {#if showRegister}
        <h1 class="text-3xl font-bold mb-8 text-center">Register</h1>
        <div class="mb-4">
          <Input type="text" placeholder="Username" bind:value={form.username} on:keydown={handleKeydown}>
            <svelte:fragment slot="icon">
              <UserRound class="text-gray-500" />
            </svelte:fragment>
          </Input>
          {#if errors.username}<p class="text-center text-red-600 bg-red-200 rounded-lg py-1 text-sm mt-1">{errors.username}</p>{/if}
        </div>
        <div class="mb-4">
          <Input type="text" placeholder="Email" bind:value={form.email} on:keydown={handleKeydown}>
            <svelte:fragment slot="icon">
              <Mail class="text-gray-500" />
            </svelte:fragment>
          </Input>
          {#if errors.email}<p class="text-center text-red-600 bg-red-200 rounded-lg py-1 text-sm mt-1">{errors.email}</p>{/if}
        </div>
        <div class="mb-4">
          <Input type="password" placeholder="Password" bind:value={form.password} on:keydown={handleKeydown}>
            <svelte:fragment slot="icon">
              <Lock class="text-gray-500" />
            </svelte:fragment>
          </Input>
          {#if errors.password}<p class="text-center text-red-600 bg-red-200 rounded-lg py-1 text-sm mt-1">{errors.password}</p>{/if}
        </div>
        <div class="mb-4">
          <Input type="password" placeholder="Confirm Password" bind:value={form.confirmPassword} on:keydown={handleKeydown}>
            <svelte:fragment slot="icon">
              <Lock class="text-gray-500" />
            </svelte:fragment>
          </Input>
          {#if errors.confirmPassword}<p class="text-center text-red-600 bg-red-200 rounded-lg py-1 text-sm mt-1">{errors.confirmPassword}</p>{/if}
        </div>
        <div class="flex justify-center items-center">
          <Button
            on:click={register}
            class="mt-4 px-4 py-8 text-xl text-white font-semibold rounded-full w-1/2 hover:opacity-80 transition bg-gradient-to-tr from-[#020024] via-[#0000d5] to-[#6a00ff]"
          >
            Register
          </Button>
        </div>
        <div class="text-center mt-8">
          <Button type="button" class="bg-white text-blue-500 hover:underline hover:bg-white" on:click={registerLoginSwitch}>Already have an account? Login here</Button>
        </div>
      {:else}
        <h1 class="text-3xl font-bold mb-8 text-center">Login</h1>
        <div class="mb-4">
          <Input type="text" placeholder="Username or Email" bind:value={form.usernameOrEmail} on:keydown={handleKeydown}>
            <svelte:fragment slot="icon">
              <UserRound class="text-gray-500" />
            </svelte:fragment>
          </Input>
          {#if errors.usernameOrEmail}<p class="text-center text-red-600 bg-red-200 rounded-lg py-1 text-sm mt-1">{errors.usernameOrEmail}</p>{/if}
        </div>
        <div class="mb-4">
          <Input type="password" placeholder="Password" bind:value={form.password} on:keydown={handleKeydown}>
            <svelte:fragment slot="icon">
              <Lock class="text-gray-500" />
            </svelte:fragment>
          </Input>
          {#if errors.password}<p class="text-center text-red-600 bg-red-200 rounded-lg py-1 text-sm mt-1">{errors.password}</p>{/if}
        </div>
        <div class="flex justify-center items-center">
          <Button
            on:click={login}
            class="mt-8 px-4 py-8 text-xl text-white font-semibold rounded-full w-1/2 hover:opacity-80 transition bg-gradient-to-tr from-[#020024] via-[#0000d5] to-[#6a00ff]"
          >
            Login
          </Button>
        </div>
        <div class="text-center mt-8">
          <Button type="button" class="bg-white text-blue-500 hover:underline hover:bg-white" on:click={registerLoginSwitch}>Don't have an account? Register here</Button>
        </div>
      {/if}
      {#if errors.form}<p class="text-center text-red-600 bg-red-200 rounded-lg py-1 text-sm mt-4">{errors.form}</p>{/if}
    </div>
    <div class="w-1/2 overflow-hidden shadow-lg">
      <div class="w-full h-full rounded-r-lg bg-gradient-to-tr from-[#020024] via-[#0000d5] to-[#6a00ff]"></div>
    </div>
  </div>
</div>