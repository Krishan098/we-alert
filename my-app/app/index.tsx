import { useEffect } from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import { Redirect, useRouter } from 'expo-router';
import { AuthContext } from '../src/context/AuthContext';
import { useContext } from 'react';

export default function Index() {
  const { isAuthenticated, isLoading } = useContext(AuthContext);
  
  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#1e88e5" />
      </View>
    );
  }
  
  if (isAuthenticated) {
    return <Redirect href="../home" />;
  }
  
  return <Redirect href="../login" />;
}