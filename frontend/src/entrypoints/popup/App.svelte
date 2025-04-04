<script context="module" lang="ts">
  // Declare Chrome API types
  declare const chrome: {
    tabs: {
      query: (queryInfo: { active: boolean; currentWindow: boolean }) => Promise<Array<{ url?: string }>>;
    };
  };
</script>

<script lang="ts">
  import { onMount } from 'svelte';
  
  let currentUrl: string = '';
  let companies: any[] = [];
  let loading: boolean = false;
  let error: string | null = null;
  
  // Function to get the current tab URL
  async function getCurrentTabUrl() {
    try {
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tabs[0]?.url) {
        currentUrl = tabs[0].url;
        return currentUrl;
      }
      return null;
    } catch (err) {
      console.error('Error getting current tab URL:', err);
      return null;
    }
  }
  
  // Function to extract company information
  async function extractCompanyInfo() {
    loading = true;
    error = null;
    companies = [];
    
    try {
      // Get the current tab URL
      const url = await getCurrentTabUrl();
      if (!url) {
        error = 'Could not get current tab URL';
        loading = false;
        return;
      }
      
      // Extract the domain from the URL
      const domain = new URL(url).hostname;
      
      // Send request to the API
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: domain }),
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      companies = data.companies;
    } catch (err) {
      console.error('Error extracting company info:', err);
      error = err instanceof Error ? err.message : 'Unknown error occurred';
    } finally {
      loading = false;
    }
  }
  
  // Get the current URL when the component mounts
  onMount(async () => {
    await getCurrentTabUrl();
  });
</script>

<main>
  <div class="container">
    <h1>Company Extractor</h1>
    
    <div class="url-display">
      <p>Current URL: <span class="url">{currentUrl || 'Loading...'}</span></p>
    </div>
    
    <button 
      class="extract-button" 
      on:click={extractCompanyInfo} 
      disabled={loading || !currentUrl}
    >
      {loading ? 'Extracting...' : 'Extract Company Info'}
    </button>
    
    {#if error}
      <div class="error">
        <p>Error: {error}</p>
      </div>
    {/if}
    
    {#if companies.length > 0}
      <div class="results">
        <h2>Extracted Companies</h2>
        {#each companies as company}
          <div class="company-card">
            <h3>{company.name}</h3>
            <p><strong>Industry:</strong> {company.industry}</p>
            <p><strong>Funding:</strong> ${company.funding.toLocaleString()}</p>
            <p><strong>Founded:</strong> {company.founded}</p>
          </div>
        {/each}
      </div>
    {:else if !loading && !error}
      <div class="empty-state">
        <p>Click the button above to extract company information</p>
      </div>
    {/if}
  </div>
</main>

<style>
  .container {
    width: 400px;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }
  
  h2 {
    font-size: 20px;
    margin-top: 20px;
    margin-bottom: 15px;
    color: #444;
  }
  
  .url-display {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
    word-break: break-all;
  }
  
  .url {
    font-weight: bold;
    color: #0066cc;
  }
  
  .extract-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    width: 100%;
    transition: background-color 0.3s;
  }
  
  .extract-button:hover:not(:disabled) {
    background-color: #45a049;
  }
  
  .extract-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .error {
    background-color: #ffebee;
    color: #c62828;
    padding: 10px;
    border-radius: 4px;
    margin-top: 15px;
  }
  
  .company-card {
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
  }
  
  .company-card h3 {
    margin-top: 0;
    color: #333;
  }
  
  .company-card p {
    margin: 8px 0;
  }
  
  .empty-state {
    text-align: center;
    color: #666;
    margin-top: 20px;
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 4px;
  }
</style>
