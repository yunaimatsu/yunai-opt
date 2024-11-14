const fetch = require('node-fetch'); // Use require() for CommonJS

// Replace with your own values
const NOTION_TOKEN = "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";
const PARENT_PAGE_ID = "121ca673ec078012a4bfc9dfa01edd9a";

const url = `https://api.notion.com/v1/blocks/${PARENT_PAGE_ID}/children`;
const headers = {
    "Authorization": `Bearer ${NOTION_TOKEN}`,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  // Replace with the latest version if needed
};

// The request body to add a "Hello World" paragraph block
const data = {
    "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Hello World"
                        }
                    }
                ]
            }
        }
    ]
};

// Function to send the request to add the block
async function addBlock() {
    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: headers,
            body: JSON.stringify(data)
        });

        // Print the response status and data
        console.log(response.status);
        const responseData = await response.json();
        console.log(responseData);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Call the function to add the block
addBlock();
