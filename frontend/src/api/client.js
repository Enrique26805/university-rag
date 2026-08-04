import axios from 'axios'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
})

export class ValidationError extends Error {
  constructor(message, details) {
    super(message)
    this.name = 'ValidationError'
    this.details = details
  }
}

export class BackendUnavailableError extends Error {
  constructor(message) {
    super(message)
    this.name = 'BackendUnavailableError'
  }
}

export async function askQuestion(question) {
  try {
    const response = await apiClient.post('/ask', { question })
    return response.data
  } catch (error) {
    const status = error.response?.status

    if (status === 422) {
      throw new ValidationError(
        'Please enter a valid question.',
        error.response.data?.detail,
      )
    }

    if (status === 503) {
      throw new BackendUnavailableError(
        error.response.data?.detail || 'The backend is currently unavailable.',
      )
    }

    throw error
  }
}
