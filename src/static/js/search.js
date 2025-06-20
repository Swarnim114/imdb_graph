document.addEventListener('DOMContentLoaded', function() {
  // Get network instance after it's created
  setTimeout(() => {
    const network = window.network;
    if (!network) {
      console.error("Network visualization not found");
      return;
    }
    
    const nodes = network.body.data.nodes;
    
    // Function to search and highlight nodes
    function searchAndHighlight() {
      const searchText = document.getElementById('searchInput').value.toLowerCase();
      const searchResults = document.getElementById('searchResults');
      searchResults.innerHTML = '';
      
      if (searchText.length < 2) {
          searchResults.style.display = 'none';
          return;
      }
      
      // Clear any previous highlights
      nodes.getIds().forEach(id => {
          const node = nodes.get(id);
          if (node.originalColor) {
              nodes.update({
                  id: id,
                  color: node.originalColor
              });
          }
      });
      
      // Find matching nodes
      const matchingNodes = [];
      nodes.getIds().forEach(id => {
          const node = nodes.get(id);
          if (node.label && node.label.toLowerCase().includes(searchText)) {
              matchingNodes.push({
                  id: id,
                  label: node.label
              });
          }
      });
      
      // Display results
      if (matchingNodes.length > 0) {
          searchResults.style.display = 'block';
          const resultsTitle = document.createElement('div');
          resultsTitle.id = 'searchTitle';
          resultsTitle.textContent = `Found ${matchingNodes.length} movies`;
          searchResults.appendChild(resultsTitle);
          
          matchingNodes.forEach(node => {
              const resultItem = document.createElement('div');
              resultItem.className = 'resultItem';
              resultItem.textContent = node.label;
              resultItem.onclick = function() {
                  // Store original colors if not already stored
                  nodes.getIds().forEach(id => {
                      const n = nodes.get(id);
                      if (!n.originalColor) {
                          n.originalColor = n.color;
                          nodes.update(n);
                      }
                  });
                  
                  // Reset all nodes to original color
                  nodes.getIds().forEach(id => {
                      const n = nodes.get(id);
                      nodes.update({
                          id: id,
                          color: n.originalColor
                      });
                  });
                  
                  // Highlight selected node with a much more vibrant color
                  nodes.update({
                      id: node.id,
                      color: {
                          background: '#00FFFF', // Bright cyan color for high visibility
                          border: '#0000FF',     // Blue border
                          highlight: {
                              background: '#00FFFF',
                              border: '#0000FF'
                          }
                      },
                      borderWidth: 3,           // Thicker border
                      size: 25                  // Slightly larger node
                  });
                  
                  // Focus on the node with increased zoom
                  network.focus(node.id, {
                      scale: 15.0,              // Increased zoom level
                      animation: {
                          duration: 1000,
                          easingFunction: 'easeInOutQuad'
                      }
                  });
                  
                  // Highlight active result item
                  document.querySelectorAll('.resultItem').forEach(item => {
                      item.classList.remove('active');
                  });
                  resultItem.classList.add('active');
              };
              searchResults.appendChild(resultItem);
          });
      } else {
          searchResults.style.display = 'block';
          searchResults.innerHTML = '<div class="searchDescription">No movies found matching your search.</div>';
      }
    }
    
    // Save original colors for all nodes
    nodes.getIds().forEach(id => {
      const node = nodes.get(id);
      node.originalColor = node.color;
      nodes.update(node);
    });
    
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const searchResults = document.getElementById('searchResults');
    
    // Search button click handler
    searchBtn.addEventListener('click', searchAndHighlight);
    
    // Handle enter key in search box
    searchInput.addEventListener('keyup', function(e) {
      if (e.key === 'Enter') {
        searchAndHighlight();
      } else if (searchInput.value.length >= 2) {
        // Auto-search after typing 2+ characters (with small delay)
        clearTimeout(searchInput.searchTimeout);
        searchInput.searchTimeout = setTimeout(searchAndHighlight, 300);
      }
    });
    
    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchResults.contains(e.target) && e.target !== searchBtn && e.target !== searchInput) {
        searchResults.style.display = 'none';
      }
    });
    
    // Focus search input when pressing '/' key
    document.addEventListener('keydown', function(e) {
      if (e.key === '/' && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput.focus();
      }
      
      // ESC key to clear search and hide results
      if (e.key === 'Escape') {
        searchInput.value = '';
        searchResults.style.display = 'none';
        // Reset all nodes to original color
        nodes.getIds().forEach(id => {
            const n = nodes.get(id);
            nodes.update({
                id: id,
                color: n.originalColor
            });
        });
      }
    });
    
    // Add keyboard shortcut hint to placeholder
    searchInput.placeholder = "Search for a movie... (Press '/' to focus)";
  }, 1000); // Give time for the network to initialize
});
