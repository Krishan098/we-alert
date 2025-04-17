import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { useContext } from 'react';
import { AuthContext } from '../src/context/AuthContext';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const { logout } = useContext(AuthContext);
  const router = useRouter();
  
  const handleLogout = async () => {
    await logout();
    router.replace('../login');
  };
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to We Alert</Text>
      <Text style={styles.subtitle}>You are logged in</Text>
      <Button title="Logout" onPress={handleLogout} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 20,
    color: '#666',
  },
});