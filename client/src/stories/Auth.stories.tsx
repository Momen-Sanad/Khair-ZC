import type { Meta, StoryObj } from '@storybook/react';
import Auth from '../components/Auth'; // Adjust the import path to match your project structure
import React from 'react';

const meta: Meta<typeof Auth> = {
  title: 'Components/Auth',
  component: Auth,
  parameters: {
    layout: 'centered',
  },
  decorators: [
    (Story) => (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        backgroundColor: '#f0f2f5'
      }}>
        <Story />
      </div>
    ),
  ],
};

export default meta;

type Story = StoryObj<typeof meta>;

export const SignIn: Story = {
  name: 'Sign In View',
  render: () => <Auth />,
};

export const SignUp: Story = {
  name: 'Sign Up View',
  render: () => {
    // Simulate signing up by manipulating component state
    const [isSignUp, setIsSignUp] = React.useState(true);
    return <Auth />;
  },
  decorators: [
    (Story) => {
      // Force sign up view
      return React.createElement(() => {
        const [, forceRender] = React.useState({});
        
        React.useEffect(() => {
          // Manually trigger the toggle to sign up view
          const authWrapper = document.querySelector('.auth-link a');
          if (authWrapper) {
            (authWrapper as HTMLAnchorElement).click();
          }
        }, []);

        return <Story />;
      });
    },
  ],
};

export const SignInWithError: Story = {
  name: 'Sign In with Error',
  render: () => {
    // Simulate error scenario
    React.useEffect(() => {
      // You might want to mock the fetch or add error handling logic here
      // This is a placeholder for demonstrating error state
      console.log('Simulating authentication error');
    }, []);

    return <Auth />;
  },
};