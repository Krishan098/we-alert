import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  KeyboardAvoidingView, 
  Platform,
  ScrollView,
  Alert
} from 'react-native';
import CustomInput from '../../components/common/CustomInput';
import CustomButton from '../../components/common/CustomButton';
import { Ionicons } from '@expo/vector-icons';
import { StackNavigationProp} from '@react-navigation/stack';
import {api} from '../../services/api'

type RegisterScreenNavigationProp = StackNavigationProp<any, any>;

export default function RegisterScreen({ navigation }: { navigation: RegisterScreenNavigationProp }) {
  const [fullName, setFullName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const handleRegister = async () => {
    if (!fullName || !phoneNumber || !email) {
      Alert.alert('Error', 'Please fill all the required fields');
      return;
    }
    
    if (phoneNumber.length < 10) {
      Alert.alert('Error', 'Please enter a valid phone number');
      return;
    }
    
    if (!email.includes('@')) {
      Alert.alert('Error', 'Please enter a valid email address');
      return;
    }
    
    setIsLoading(true);
    
    try {
        const formattedNumber = phoneNumber.startsWith('+') ? phoneNumber : `+${phoneNumber}`;
        
        // Call your API to register the user with email
        const response = await api.post('/api/auth/register/', {
          phone_number: formattedNumber,
          name: fullName,
          email: email
        });
        
        if (response.data.success) {
          
          navigation.navigate('OTP', { phoneNumber: formattedNumber });
        } else {
          Alert.alert('Error', response.data.error || 'Registration failed');
        }
      } catch (error) {
        Alert.alert('Error', 'Registration failed. Please try again.');
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    };
  
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <TouchableOpacity 
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Ionicons name="arrow-back" size={24} color="#333" />
        </TouchableOpacity>
        
        <View style={styles.formContainer}>
          <Text style={styles.title}>Create Account</Text>
          <Text style={styles.subtitle}>Sign up to get started</Text>
          
          <CustomInput
            value={fullName}
            onChangeText={setFullName}
            placeholder="Full Name"
            lefticon={<Ionicons name="person-outline" size={24} color="#666" />}
          />
          
          <CustomInput
            value={phoneNumber}
            onChangeText={setPhoneNumber}
            placeholder="Phone Number"
            keyboardType="phone-pad"
            lefticon={<Ionicons name="call-outline" size={24} color="#666" />}
          />
          
          <CustomInput
            value={email}
            onChangeText={setEmail}
            placeholder="Email"
            keyboardType="email-address"
            lefticon={<Ionicons name="mail-outline" size={24} color="#666" />}
          />
          
          <CustomButton
            title="Sign Up"
            onPress={handleRegister}
            loading={isLoading}
          />
          
          <TouchableOpacity 
            style={styles.loginLink}
            onPress={() => navigation.navigate('Login')}
          >
            <Text style={styles.loginText}>
              Already have an account? <Text style={styles.loginHighlight}>Sign In</Text>
            </Text>
          </TouchableOpacity>
        </View>
        
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            By signing up, you agree to our Terms of Service and Privacy Policy
          </Text>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  scrollContent: {
    flexGrow: 1,
  },
  backButton: {
    padding: 20,
  },
  formContainer: {
    padding: 20,
    marginBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 30,
  },
  loginLink: {
    marginTop: 20,
    alignItems: 'center',
  },
  loginText: {
    fontSize: 14,
    color: '#666',
  },
  loginHighlight: {
    color: '#1e88e5',
    fontWeight: 'bold',
  },
  footer: {
    padding: 20,
  },
  footerText: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
  },
});