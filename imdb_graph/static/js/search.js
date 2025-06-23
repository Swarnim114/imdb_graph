/**
 * Search functionality for IMDB Movie Graph visualization.
 * 
 * This script adds interactive search capabilities to the movie graph,
 * allowing users to find and highlight specific movies in the visualization.
 */

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
                      color: '#FFFF00'
                  });
                  
                  // Focus on the selected node
                  network.focus(node.id, {
                      scale: 1.2,
                      animation: {
                          duration: 800,
                          easingFunction: 'easeInOutQuad'
                      }
                  });
                  
                  // Add the highlight class for animation
                  const nodeDOM = document.querySelector(`[data-id="${node.id}"]`);
                  if (nodeDOM) {
                      nodeDOM.classList.add('highlight');
                      // Remove highlight class after animation completes
                      setTimeout(() => {
                          nodeDOM.classList.remove('highlight');
                      }, 4500);
                  }
              };
              searchResults.appendChild(resultItem);
          });
      } else {
          searchResults.style.display = 'block';
          const noResults = document.createElement('div');
          noResults.className = 'resultItem';
          noResults.style.cursor = 'default';
          noResults.textContent = 'No movies found';
          searchResults.appendChild(noResults);
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
        // Auto-search for 2+ characters
        searchAndHighlight();
      } else if (searchInput.value.length === 0) {
        // Clear results when input is empty
        searchResults.style.display = 'none';
        searchResults.innerHTML = '';
        
        // Reset all nodes to original color
        nodes.getIds().forEach(id => {
            const node = nodes.get(id);
            if (node.originalColor) {
                nodes.update({
                    id: id,
                    color: node.originalColor
                });
            }
        });
      }
    });
    
    // Clear results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchContainer.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.style.display = 'none';
      }
    });
    
    // Add keyboard shortcut for search ('/' key)
    document.addEventListener('keydown', function(e) {
      // Check if user is not typing in an input field
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        searchInput.focus();
      }
      // ESC key to clear search and hide results
      if (e.key === 'Escape') {
        searchInput.value = '';
        searchResults.style.display = 'none';
        
        // Reset all nodes to original color
        nodes.getIds().forEach(id => {
            const node = nodes.get(id);
            if (node.originalColor) {
                nodes.update({
                    id: id,
                    color: node.originalColor
                });
            }
        });
      }
    });
  }, 1000); // Wait for network to be initialized
});
