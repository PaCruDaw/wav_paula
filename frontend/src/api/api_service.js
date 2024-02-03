import axios from 'axios';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: 'https://thronesapi.com/api/v2',  // Replace with your API base URL
      headers: {
        'Content-Type': 'application/json',
        // Add any other headers you need
      },
    });
  }

  // Example of a GET request
  async fetchData(endpoint) {
    try {
      const response = await this.api.get(endpoint);
      return response;
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  }

  // Example of a POST request
  async postData(endpoint, data) {
    try {
      const response = await this.api.post(endpoint, data);
      return response.data;
    } catch (error) {
      console.error('Error posting data:', error);
      throw error;
    }
  }

}

// Create a singleton instance of the service
const apiService = new ApiService();
export default apiService;
