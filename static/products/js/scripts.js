
// let products = [
//     { 
//         name: 'Seamailer', 
//         description: 'Send marketing emails that bring results without limits.', 
//         votes: 541, 
//         isPromoted: true, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Video SDK 3.0', 
//         description: 'Build and integrate real-time multimodal AI characters.', 
//         votes: 489, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Temperstack', 
//         description: 'Enterprise-grade SRE process automation for Dev & SRE teams.', 
//         votes: 396, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Guidde', 
//         description: 'Magically create stunning how-to videos with AI.', 
//         votes: 3463, 
//         isPromoted: true, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Graphite Reviewer', 
//         description: 'Your high-signal AI code review companion.', 
//         votes: 381, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Inbox Zero', 
//         description: 'An open-source, AI personal assistant for email.', 
//         votes: 315, 
//         isPromoted: true,  
//         logo: 'https://via.placeholder.com/60'
//     },
//     // New Products
//     { 
//         name: 'Flare Notify', 
//         description: 'Push notification service for web and mobile.', 
//         votes: 297, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Bright Analytics', 
//         description: 'Data analytics platform with a real-time dashboard.', 
//         votes: 620, 
//         isPromoted: true,  
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Robo Writer', 
//         description: 'AI-powered content writing tool for bloggers.', 
//         votes: 1340, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Code Mirror', 
//         description: 'Real-time collaborative coding environment.', 
//         votes: 289, 
//         isPromoted: true,  
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Auto Translate', 
//         description: 'Instant translation service for websites and apps.', 
//         votes: 735, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Pixify', 
//         description: 'AI tool for creating pixel art from photos.', 
//         votes: 415, 
//         isPromoted: true,  
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'Data Whisper', 
//         description: 'AI-based data visualization tool.', 
//         votes: 1182, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'AI Tutor', 
//         description: 'AI-based personal tutoring assistant for students.', 
//         votes: 525, 
//         isPromoted: true, 
//         logo: 'https://via.placeholder.com/60'
//     },
//     { 
//         name: 'FlowChart Genius', 
//         description: 'AI tool for auto-generating flowcharts.', 
//         votes: 677, 
//         isPromoted: false, 
//         logo: 'https://via.placeholder.com/60'
//     },
// ];

// function renderProducts() {
//     const productList = document.getElementById('product-list');
//     productList.innerHTML = '';  

//     products.forEach((product, index) => {
//         const productItem = document.createElement('div');
//         productItem.classList.add('product-item');
        
//         productItem.innerHTML = `
//             <img src="${product.logo}" alt="Product Logo" class="product-logo">
//             <div class="product-content">
//                 <h3>${product.name} ${product.isPromoted ? '<span class="promoted-badge">Promoted</span>' : ''}</h3>
//                 <p>${product.description}</p>
//             </div>
//             <div class="vote">
//                 <span>${product.votes} Upvotes</span>
//                 <button onclick="upvote(${index})">Upvote</button>
//             </div>
//         `;
//         productList.appendChild(productItem);
//     });
// }


// function upvote(index) {
//     products[index].votes += 1;
//     renderProducts();
// }


// renderProducts();
