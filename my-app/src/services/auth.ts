import AsyncStorage from '@react-native-async-storage/async-storage';
import { api } from './api';

export const AUTH_TOKEN_KEY = 'auth_token';
export const REFRESH_TOKEN_KEY = 'refresh_token';
export const USER_DATA_KEY = 'user_data';

export const authService = {
  async sendOTP(phoneNumber: string): Promise<any> {
    try {
      console.log('Sending OTP request to:', '/api/auth/send-otp/');
      console.log('Phone number:', phoneNumber);
      const response = await api.post('/api/auth/send-otp/', { phone_number: phoneNumber });
      console.log('OTP response data:', response.data);
      
      return {
        success: true,
        is_new_user: response.data.is_new_user || false
      };
    } catch (error: any) {
      console.error('Error sending OTP:', error);
      if (error.response) {
        console.error('Error response data:', error.response.data);
      }
      return { 
        success: false, 
        error: error.response?.data?.error || error.message 
      };
    }
  },

  async verifyOTP(phoneNumber: string, otp: string): Promise<any> {
    try {
      const response = await api.post('/api/auth/verify-otp/', { 
        phone_number: phoneNumber, 
        otp 
      });

      // Define the expected response type
      type VerifyOTPResponse = {
        message: string;
        token: {
          access: string;
          refresh: string;
        };
        user: any;
      };

      const data = response.data as VerifyOTPResponse;

      // Store tokens and user data
      await AsyncStorage.setItem(AUTH_TOKEN_KEY, data.token.access);
      await AsyncStorage.setItem(REFRESH_TOKEN_KEY, data.token.refresh);
      await AsyncStorage.setItem(USER_DATA_KEY, JSON.stringify(response.data.user));
      
      return {
        success:true,
        user:response.data.user,
      };
    } catch (error:any) {
      console.error('Error verifying OTP:', error);
      return {success :false};
    }
  },

  async refreshToken(): Promise<boolean> {
    try {
      const refreshToken = await AsyncStorage.getItem(REFRESH_TOKEN_KEY);
      
      if (!refreshToken) {
        return false;
      }
      
      const response = await api.post('/auth/token/refresh/', { 
        refresh: refreshToken 
      });

      // Define the expected response type
      type RefreshTokenResponse = {
        access: string;
      };

      const data = response.data as RefreshTokenResponse;

      await AsyncStorage.setItem(AUTH_TOKEN_KEY, data.access);
      return true;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  },

  async logout(): Promise<void> {
    try{

    
    await AsyncStorage.removeItem(AUTH_TOKEN_KEY);
    await AsyncStorage.removeItem(REFRESH_TOKEN_KEY);
    await AsyncStorage.removeItem(USER_DATA_KEY);
  }catch (error) {
    console.error('Error during logout:', error);
  }
},
  async isLoggedIn(): Promise<boolean> {
    const token = await AsyncStorage.getItem(AUTH_TOKEN_KEY);
    return !!token;
  },

  async getCurrentUser(): Promise<any> {
    const userData = await AsyncStorage.getItem(USER_DATA_KEY);
    return userData ? JSON.parse(userData) : null;
  }
};