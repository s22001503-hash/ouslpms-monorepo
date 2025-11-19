/**
 * Google Drive API Service
 * Handles file uploads to Google Drive
 */

// Load Google API
const loadGoogleAPI = () => {
  return new Promise((resolve, reject) => {
    if (window.gapi) {
      resolve(window.gapi)
      return
    }

    const script = document.createElement('script')
    script.src = 'https://apis.google.com/js/api.js'
    script.onload = () => {
      window.gapi.load('client:auth2', () => {
        resolve(window.gapi)
      })
    }
    script.onerror = reject
    document.body.appendChild(script)
  })
}

// Initialize Google Drive API
export const initGoogleDrive = async () => {
  try {
    const gapi = await loadGoogleAPI()
    
    await gapi.client.init({
      apiKey: import.meta.env.VITE_GOOGLE_API_KEY,
      clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'],
      scope: 'https://www.googleapis.com/auth/drive.file'
    })

    return gapi
  } catch (error) {
    console.error('Error initializing Google Drive API:', error)
    throw error
  }
}

// Sign in to Google
export const signInToGoogle = async () => {
  try {
    const gapi = window.gapi
    const auth = gapi.auth2.getAuthInstance()
    
    if (!auth.isSignedIn.get()) {
      await auth.signIn()
    }
    
    return auth.currentUser.get()
  } catch (error) {
    console.error('Error signing in to Google:', error)
    throw error
  }
}

// Upload file to Google Drive
export const uploadToDrive = async (file, fileName) => {
  try {
    // Ensure user is signed in
    await signInToGoogle()

    const boundary = '-------314159265358979323846'
    const delimiter = "\r\n--" + boundary + "\r\n"
    const close_delim = "\r\n--" + boundary + "--"

    // Read file content
    const reader = new FileReader()
    const fileContent = await new Promise((resolve, reject) => {
      reader.onload = (e) => resolve(e.target.result)
      reader.onerror = reject
      reader.readAsDataURL(file)
    })

    // Extract base64 content
    const base64Data = fileContent.split(',')[1]

    // Metadata
    const metadata = {
      name: fileName || file.name,
      mimeType: file.type,
      description: 'Uploaded via EcoPrint - Print Management System'
    }

    // Multipart request body
    const multipartRequestBody =
      delimiter +
      'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
      JSON.stringify(metadata) +
      delimiter +
      'Content-Type: ' + file.type + '\r\n' +
      'Content-Transfer-Encoding: base64\r\n\r\n' +
      base64Data +
      close_delim

    // Upload to Drive
    const response = await window.gapi.client.request({
      path: '/upload/drive/v3/files',
      method: 'POST',
      params: { uploadType: 'multipart' },
      headers: {
        'Content-Type': 'multipart/related; boundary="' + boundary + '"'
      },
      body: multipartRequestBody
    })

    return response.result
  } catch (error) {
    console.error('Error uploading to Google Drive:', error)
    throw error
  }
}

// Get file link from Drive
export const getFileLinkFromDrive = (fileId) => {
  return `https://drive.google.com/file/d/${fileId}/view`
}

// Check if Google Drive is available
export const isGoogleDriveAvailable = () => {
  return !!(import.meta.env.VITE_GOOGLE_CLIENT_ID && import.meta.env.VITE_GOOGLE_API_KEY)
}

// Simplified upload with error handling
export const saveToDrive = async (file, options = {}) => {
  const {
    fileName = file.name,
    onProgress = () => {},
    onSuccess = () => {},
    onError = () => {}
  } = options

  try {
    // Check if credentials are configured
    if (!isGoogleDriveAvailable()) {
      throw new Error('Google Drive credentials not configured. Please contact administrator.')
    }

    onProgress('Initializing Google Drive...')
    await initGoogleDrive()

    onProgress('Requesting permission...')
    await signInToGoogle()

    onProgress('Uploading file...')
    const result = await uploadToDrive(file, fileName)

    const fileLink = getFileLinkFromDrive(result.id)
    
    onSuccess({
      fileId: result.id,
      fileName: result.name,
      fileLink,
      message: 'File saved to Google Drive successfully!'
    })

    return {
      success: true,
      fileId: result.id,
      fileLink
    }

  } catch (error) {
    console.error('Save to Drive error:', error)
    onError(error.message || 'Failed to save to Google Drive')
    
    return {
      success: false,
      error: error.message
    }
  }
}

export default {
  initGoogleDrive,
  signInToGoogle,
  uploadToDrive,
  getFileLinkFromDrive,
  isGoogleDriveAvailable,
  saveToDrive
}
