import React from 'react';
import { View, TextInput, StyleSheet, Text } from 'react-native';

type CustomInputProps = {
  value: string;
  onChangeText: (text: string) => void;
  placeholder: string;
  secureTextEntry?: boolean;
  keyboardType?: 'default' | 'number-pad' | 'decimal-pad' | 'numeric' | 'email-address' | 'phone-pad';
  maxLength?: number;
  editable?: boolean;
  autoCapitalize?: 'none' | 'sentences' | 'words' | 'characters';
  error?: string;
  lefticon?: React.ReactNode;
  righticon?: React.ReactNode;
};

const CustomInput: React.FC<CustomInputProps> = ({
  value,
  onChangeText,
  placeholder,
  secureTextEntry = false,
  keyboardType = 'default',
  maxLength,
  editable = true,
  autoCapitalize = 'none',
  error,
  lefticon,
  righticon,
}) => {
  return (
    <View style={styles.container}>
      {lefticon && <View style={styles.iconContainer}>{lefticon}</View>}
      <TextInput
        style={[styles.input, error ? styles.inputError : null,
          lefticon? styles.inputWithIcon : null,
        ]}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor="#999"
        secureTextEntry={secureTextEntry}
        keyboardType={keyboardType}
        maxLength={maxLength}
        editable={editable}
        autoCapitalize={autoCapitalize}
      />
      {righticon && <View style={styles.iconContainer}>{righticon}</View>}
      {error ? <Text style={styles.errorText}>{error}</Text> : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginVertical: 10,
  },
  input: {
    backgroundColor: '#f9f9f9',
    height: 50,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
    paddingHorizontal: 15,
    fontSize: 16,
  },
  inputWithIcon: {
    paddingLeft: 40, // Make room for the icon
  },
  iconContainer: {
    position: 'absolute',
    left: 15,
    zIndex: 1,
  },
  inputError: {
    borderColor: '#ff3b30',
  },
  errorText: {
    color: '#ff3b30',
    marginTop: 5,
    fontSize: 12,
  },
});

export default CustomInput;