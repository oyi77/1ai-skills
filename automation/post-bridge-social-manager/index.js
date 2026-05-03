/**
 * Post Bridge Social Manager
 * Post to multiple social media platforms via post-bridge.com API
 * 
 * API Key: pb_live_LzxK4Q4428kb1b6KETgdue
 * Base URL: https://api.post-bridge.com/v1
 */

const axios = require('axios');

class PostBridgeManager {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://api.post-bridge.com/v1';
    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * Get connected social accounts
   */
  async getSocialAccounts() {
    try {
      const response = await this.client.get('/social-accounts');
      return response.data;
    } catch (error) {
      console.error('Error getting accounts:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Create a new post
   * @param {Object} options
   * @param {string} options.caption - Post content/caption
   * @param {number[]} options.social_accounts - Array of account IDs
   * @param {string[]} options.media_urls - Optional media URLs
   * @param {string} options.scheduled_at - ISO timestamp for scheduling
   */
  async createPost({ caption, social_accounts, media_urls = [], scheduled_at = null }) {
    try {
      const payload = {
        caption,
        social_accounts
      };

      if (media_urls.length > 0) {
        payload.media = media_urls.map(url => ({ url }));
      }

      if (scheduled_at) {
        payload.scheduled_at = scheduled_at;
      }

      const response = await this.client.post('/posts', payload);
      return response.data;
    } catch (error) {
      console.error('Error creating post:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * List recent posts
   * @param {number} limit - Number of posts to retrieve
   */
  async listPosts(limit = 10) {
    try {
      const response = await this.client.get('/posts', {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error listing posts:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get post details
   * @param {string} postId - Post ID
   */
  async getPost(postId) {
    try {
      const response = await this.client.get(`/posts/${postId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting post:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Delete a post
   * @param {string} postId - Post ID to delete
   */
  async deletePost(postId) {
    try {
      const response = await this.client.delete(`/posts/${postId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting post:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Quick broadcast to all connected accounts
   * @param {string} caption - Post content
   * @param {string[]} media_urls - Optional media URLs
   */
  async broadcast(caption, media_urls = []) {
    const accounts = await this.getSocialAccounts();
    const accountIds = accounts.data.map(a => a.id);
    return this.createPost({ caption, social_accounts: accountIds, media_urls });
  }
}

// Export for use in OpenClaw
module.exports = PostBridgeManager;
