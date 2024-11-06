<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { navigate } from "svelte-routing";
  import { Mail, Building2, Github, Twitter, ArrowRight, Linkedin } from "lucide-svelte";

  const team = [
    {
      name: "Alain Ballen",
      role: "Backend Engineer",
      linkedin: "https://www.linkedin.com/in/alain-ballen/",
      image: "/alain.jpg"
    },
    {
      name: "Dinuja Wattage",
      role: "Founding Engineer",
      linkedin: "https://www.linkedin.com/in/dinuja-wattage/",
      image: "/dinuja.jpg"
    },
    {
      name: "Laxit Shahi",
      role: "Technical Founder",
      linkedin: "https://www.linkedin.com/in/laxitshahi/",
      image: "/laxit.jpg"
    },
    {
      name: "Victor Chung",
      role: "Founding Engineer",
      linkedin: "https://www.linkedin.com/in/victor-chung-ca/",
      image: "/victor.jpg"
    },
    {
      name: "Ahmed Ali",
      role: "Software Engineer & Researcher",
      linkedin: "https://www.linkedin.com/in/ahmed-ali00/",
      image: "/ahmed.jpg"
    }
  ];
</script>

<div class="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
  <!-- Navigation -->
  <nav class="fixed w-full p-4 flex justify-between items-center bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm z-10">
    <div class="text-2xl font-bold text-slate-800 dark:text-slate-100">Rout3</div>
    <div class="space-x-4">
      <Button variant="ghost" on:click={() => navigate('/login')}>Login</Button>
      <Button on:click={() => navigate('/login')}>Get Started</Button>
    </div>
  </nav>
  
  <main class="flex-grow">
    <!-- Hero Section -->
    <div class="container mx-auto px-4 pt-32 pb-20 text-center relative">
      <div class="absolute inset-0 -z-10">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-100/30 to-purple-100/30 dark:from-blue-900/30 dark:to-purple-900/30 rounded-full blur-3xl transform -rotate-12"></div>
        <div class="absolute inset-0 bg-gradient-to-l from-purple-100/20 to-blue-100/20 dark:from-purple-900/20 dark:to-blue-900/20 rounded-full blur-3xl transform rotate-12"></div>
      </div>
      
      <h1 class="text-6xl md:text-7xl font-bold text-slate-900 dark:text-slate-50 mb-6">
        Welcome to <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">Rout3</span>
      </h1>
      <p class="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto leading-relaxed">
        Infrastructure for GenAI applications.
        <br />
        Keeping LLM integration simple.
      </p>
      <div class="space-x-4">
        <Button size="lg" class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8" on:click={() => navigate('/login')}>
          Get Started
          <ArrowRight class="ml-2 h-5 w-5" />
        </Button>
        <Button size="lg" variant="outline" class="px-8">
          Learn More
        </Button>
      </div>
    </div>

    <!-- Feature Section -->
    <div class="container mx-auto px-4">
      <div class="text-center grid md:grid-cols-3 gap-8 py-20">
        <div class="p-8 rounded-xl bg-white dark:bg-slate-800 shadow-sm hover:shadow-md transition-shadow">
          <h3 class="text-3xl font-semibold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">Maintenance</h3>
          <p class="text-xl text-slate-600 dark:text-slate-300">Thousands of models, dozens of APIs drains developer time.</p>
        </div>
        <div class="p-8 rounded-xl bg-white dark:bg-slate-800 shadow-sm hover:shadow-md transition-shadow">
          <h3 class="text-3xl font-semibold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">Reliability</h3>
          <p class="text-xl text-slate-600 dark:text-slate-300">When one provider goes down, what next?</p>
        </div>
        <div class="p-8 rounded-xl bg-white dark:bg-slate-800 shadow-sm hover:shadow-md transition-shadow">
          <h3 class="text-3xl font-semibold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">Cost</h3>
          <p class="text-xl text-slate-600 dark:text-slate-300">Cost differences of more than 70 times, which model is best for its price?</p>
        </div>
      </div>
    </div>

    <!-- Team Section -->
    <div class="bg-white dark:bg-slate-800/50 py-24">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-slate-900 dark:text-slate-100 mb-4">Meet Our Team</h2>
          <p class="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            The talented individuals behind Rout3, working to revolutionize LLM integration.
          </p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8">
          {#each team as member}
            <div class="flex flex-col items-center">
              <div class="mb-4 relative group">
                <img 
                  src={member.image} 
                  alt={member.name}
                  class="w-44 h-44 rounded-full object-cover filter grayscale hover:grayscale-0 transition-all duration-300"
                />
                <a 
                  href={member.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="absolute inset-0 flex items-center justify-center bg-blue-600/0 group-hover:bg-blue-600/80 rounded-full transition-all duration-300 opacity-0 group-hover:opacity-100"
                >
                  <Linkedin class="w-8 h-8 text-white" />
                </a>
              </div>
              <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100">{member.name}</h3>
              <p class="text-sm text-slate-600 dark:text-slate-400">{member.role}</p>
            </div>
          {/each}
        </div>
      </div>
    </div>

    <!-- About/Contact Section -->
    <div class="container mx-auto px-4 py-24">
      <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
        <div>
          <h2 class="text-4xl font-bold text-slate-900 dark:text-slate-100 mb-6">About Rout3</h2>
          <p class="text-lg text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
            We're a team of developers who understand the challenges of working with multiple LLM providers. 
            Our mission is to simplify AI integration, making it more accessible and manageable for developers everywhere.
          </p>
          <div class="space-y-4">
            <div class="flex items-center space-x-3">
              <Mail class="h-5 w-5 text-blue-600" />
              <a href="mailto:victorchung2013@gmail.com" class="text-blue-600 dark:text-blue-400 hover:underline">
                victorchung2013@gmail.com
              </a>
            </div>
            <div class="flex items-center space-x-3">
              <Building2 class="h-5 w-5 text-purple-600" />
              <span class="text-slate-600 dark:text-slate-400">Toronto, ON</span>
            </div>
            <div class="flex items-center space-x-3">
              <Github class="h-5 w-5 text-slate-600 dark:text-slate-400" />
              <a 
                href="https://github.com/llm-proxy/llm-proxy" 
                target="_blank" 
                rel="noopener noreferrer"
                class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
              >
                llm-proxy/llm-proxy
              </a>
            </div>
          </div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg">
          <h3 class="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-6">Why Choose Rout3?</h3>
          <ul class="space-y-4">
            <li class="flex items-start space-x-3">
              <div class="w-6 h-6 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex-shrink-0 mt-1"></div>
              <p class="text-slate-600 dark:text-slate-400">Simplified API integration with multiple LLM providers</p>
            </li>
            <li class="flex items-start space-x-3">
              <div class="w-6 h-6 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex-shrink-0 mt-1"></div>
              <p class="text-slate-600 dark:text-slate-400">Cost optimization through intelligent routing</p>
            </li>
            <li class="flex items-start space-x-3">
              <div class="w-6 h-6 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex-shrink-0 mt-1"></div>
              <p class="text-slate-600 dark:text-slate-400">Enhanced reliability with automatic failover</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="w-full bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-2 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
        <div>
          <h3 class="text-lg font-semibold mb-4 text-slate-900 dark:text-slate-100">Company</h3>
          <ul class="space-y-2">
            <li><a href="/about" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors">About</a></li>
            <li><a href="/blog" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors">Blog</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-4 text-slate-900 dark:text-slate-100">Resources</h3>
          <ul class="space-y-2">
            <li><a href="/docs" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors">Documentation</a></li>
            <li><a href="/status" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors">Status</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-4 text-slate-900 dark:text-slate-100">Legal</h3>
          <ul class="space-y-2">
            <li><a href="/privacy" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors">Privacy</a></li>
            <li><a href="/terms" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors">Terms</a></li>
          </ul>
        </div>
      </div>
      <div class="mt-8 pt-8 border-t border-slate-200 dark:border-slate-800 flex flex-col md:flex-row justify-between items-center max-w-4xl mx-auto">
        <p class="text-slate-600 dark:text-slate-400 mb-4 md:mb-0">
          © {new Date().getFullYear()} Rout3. All rights reserved.
        </p>
        <div class="flex space-x-4">
          <a href="https://github.com/llm-proxy/llm-proxy" target="_blank" rel="noopener noreferrer" class="hover:opacity-75 transition-opacity">
            <Github class="h-6 w-6 text-slate-600 dark:text-slate-400" />
          </a>
          <a href="/404" class="hover:opacity-75 transition-opacity">
            <Twitter class="h-6 w-6 text-slate-600 dark:text-slate-400" />
          </a>
        </div>
      </div>
    </div>
  </footer>
</div>