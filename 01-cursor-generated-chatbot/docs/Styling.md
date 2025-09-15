# Styling Documentation

## Overview
The application uses Streamlit's built-in styling system with minimal custom styling. The design follows Streamlit's default theme with basic configuration for page layout, icons, and component styling.

## Styling Architecture

### 1. Styling Layers
```
Streamlit Default Theme → Page Configuration → Component Styling → Custom CSS (Future)
```

### 2. Styling Approach
- **Framework-Based**: Uses Streamlit's built-in styling
- **Minimal Customization**: Limited custom styling
- **Responsive Design**: Mobile-friendly by default
- **Theme Consistency**: Follows Streamlit's design system

## Page Configuration

### 1. Page Setup
```python
st.set_page_config(
    page_title="Claude Sonnet QnA Chatbot",
    page_icon="🤖",
    layout="wide"
)
```

**Configuration Elements**:
- **Page Title**: "Claude Sonnet QnA Chatbot"
- **Page Icon**: Robot emoji (🤖)
- **Layout**: Wide layout for better space utilization

### 2. Layout Configuration
- **Layout Type**: Wide layout
- **Responsive**: Automatically responsive
- **Mobile Support**: Built-in mobile optimization
- **Theme**: Default Streamlit theme

## Component Styling

### 1. Title Styling
```python
st.title("🤖 Claude Sonnet QnA Chatbot")
```

**Styling Characteristics**:
- **Font Size**: Large, prominent title
- **Icon**: Robot emoji for visual appeal
- **Position**: Top of the page
- **Color**: Default theme colors

### 2. Information Messages
```python
st.info("💡 **Note**: This chatbot uses AWS Bedrock with rate limiting...")
```

**Styling Characteristics**:
- **Background**: Light blue background
- **Icon**: Lightbulb emoji
- **Typography**: Bold text for emphasis
- **Position**: Below title

### 3. Chat Interface
```python
# Chat input
if prompt := st.chat_input("Ask me anything..."):

# Chat messages
with st.chat_message("user"):
    st.write(prompt)

with st.chat_message("assistant"):
    st.write(response_text)
```

**Styling Characteristics**:
- **Input Field**: Styled input with placeholder text
- **Message Bubbles**: Distinct styling for user and assistant
- **Typography**: Readable font sizes and spacing
- **Layout**: Vertical message flow

### 4. Loading States
```python
with st.spinner("Thinking..."):
    # API call
    response_text = call_claude_model(prompt, st.session_state.messages[:-1])
```

**Styling Characteristics**:
- **Spinner**: Animated loading indicator
- **Text**: "Thinking..." message
- **Position**: Centered spinner
- **Duration**: Shows during API calls

### 5. Error Messages
```python
st.error(f"Error: {str(e)}")
```

**Styling Characteristics**:
- **Background**: Red background
- **Text**: White text for contrast
- **Icon**: Error icon
- **Position**: Prominent error display

## Visual Design Elements

### 1. Icons and Emojis
- **Page Icon**: 🤖 (Robot emoji)
- **Title Icon**: 🤖 (Robot emoji)
- **Info Icon**: 💡 (Lightbulb emoji)
- **Purpose**: Visual appeal and user engagement

### 2. Color Scheme
- **Primary Colors**: Streamlit default theme colors
- **Background**: Light theme background
- **Text**: Dark text for readability
- **Accents**: Blue for info, red for errors

### 3. Typography
- **Font Family**: Streamlit default fonts
- **Font Sizes**: Responsive font sizing
- **Font Weights**: Bold for emphasis
- **Line Height**: Optimized for readability

## Responsive Design

### 1. Mobile Optimization
- **Automatic**: Streamlit handles mobile optimization
- **Touch-Friendly**: Large touch targets
- **Readable**: Appropriate font sizes
- **Navigation**: Mobile-friendly navigation

### 2. Desktop Layout
- **Wide Layout**: Utilizes available screen space
- **Sidebar**: Optional sidebar for navigation
- **Main Area**: Chat interface in main area
- **Responsive**: Adapts to different screen sizes

## Styling Patterns

### 1. Component Styling Pattern
```python
# Consistent component styling
with st.chat_message("user"):
    st.write(content)

with st.chat_message("assistant"):
    st.write(content)
```

### 2. State-Based Styling
```python
# Different styling based on state
if error_occurred:
    st.error("Error message")
else:
    st.success("Success message")
```

### 3. Conditional Styling
```python
# Conditional styling based on conditions
if st.session_state.messages:
    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
```

## Custom Styling Capabilities

### 1. CSS Customization
```python
# Custom CSS (not currently implemented)
st.markdown("""
<style>
.custom-class {
    color: blue;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)
```

### 2. Theme Customization
```python
# Theme configuration (not currently implemented)
st.markdown("""
<style>
:root {
    --primary-color: #ff6b6b;
    --secondary-color: #4ecdc4;
}
</style>
""", unsafe_allow_html=True)
```

### 3. Component Customization
```python
# Custom component styling (not currently implemented)
st.markdown("""
<div class="custom-chat-container">
    <div class="custom-message">
        Custom styled message
    </div>
</div>
""", unsafe_allow_html=True)
```

## Styling Best Practices

### 1. Consistency
- **Use Default Components**: Leverage Streamlit's built-in components
- **Maintain Theme**: Stick to default theme for consistency
- **Icon Usage**: Use consistent iconography
- **Color Scheme**: Maintain consistent color usage

### 2. Accessibility
- **Color Contrast**: Ensure sufficient color contrast
- **Font Sizes**: Use readable font sizes
- **Touch Targets**: Provide adequate touch targets
- **Screen Readers**: Ensure screen reader compatibility

### 3. Performance
- **Minimal CSS**: Avoid heavy custom styling
- **Efficient Rendering**: Use Streamlit's optimized rendering
- **Lazy Loading**: Load styles efficiently
- **Caching**: Cache styles when possible

## Styling Limitations

### 1. Current Limitations
- **Limited Customization**: Minimal custom styling options
- **Theme Dependency**: Relies on Streamlit's default theme
- **CSS Restrictions**: Limited CSS customization
- **Component Constraints**: Bound by Streamlit component styling

### 2. Framework Constraints
- **Streamlit Limitations**: Bound by Streamlit's styling system
- **Theme Override**: Difficult to completely override themes
- **Custom Components**: Limited custom component creation
- **Advanced Layouts**: Limited advanced layout options

## Future Styling Enhancements

### 1. Custom Themes
```python
# Custom theme implementation
def apply_custom_theme():
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
```

### 2. Advanced Styling
- **Custom CSS**: Implement custom CSS styling
- **Theme Switching**: Add theme switching capability
- **Component Styling**: Custom component styling
- **Animation**: Add smooth animations and transitions

### 3. Responsive Enhancements
- **Breakpoint Management**: Custom breakpoint handling
- **Mobile Optimization**: Enhanced mobile experience
- **Desktop Features**: Desktop-specific features
- **Tablet Support**: Optimized tablet experience

## Styling Tools and Resources

### 1. Streamlit Styling
- **Documentation**: Streamlit styling documentation
- **Components**: Built-in component styling
- **Themes**: Default theme system
- **Custom CSS**: Limited CSS customization

### 2. External Styling
- **CSS Frameworks**: Bootstrap, Tailwind CSS
- **Icon Libraries**: Font Awesome, Material Icons
- **Color Palettes**: Color scheme generators
- **Typography**: Google Fonts, web fonts

### 3. Design Tools
- **Figma**: Design mockups and prototypes
- **Adobe XD**: User experience design
- **Sketch**: Interface design
- **Canva**: Quick design elements

## Styling Guidelines

### 1. Design Principles
- **Simplicity**: Keep design simple and clean
- **Consistency**: Maintain consistent styling patterns
- **Usability**: Prioritize usability over aesthetics
- **Accessibility**: Ensure accessibility compliance

### 2. Implementation Guidelines
- **Progressive Enhancement**: Start with basic styling, enhance gradually
- **Performance First**: Optimize for performance
- **Mobile First**: Design for mobile first
- **Testing**: Test across different devices and browsers

### 3. Maintenance Guidelines
- **Documentation**: Document custom styling decisions
- **Version Control**: Track styling changes
- **Review Process**: Review styling changes
- **Performance Monitoring**: Monitor styling performance impact

## Styling Examples

### 1. Basic Styling
```python
# Basic component styling
st.title("🤖 Chatbot")
st.info("Welcome to the chatbot!")
st.chat_input("Ask me anything...")
```

### 2. Advanced Styling
```python
# Advanced styling with custom CSS
st.markdown("""
<style>
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
.message {
    margin: 10px 0;
    padding: 15px;
    border-radius: 10px;
}
.user-message {
    background-color: #e3f2fd;
    margin-left: 20%;
}
.assistant-message {
    background-color: #f3e5f5;
    margin-right: 20%;
}
</style>
""", unsafe_allow_html=True)
```

### 3. Responsive Styling
```python
# Responsive styling
st.markdown("""
<style>
@media (max-width: 768px) {
    .chat-container {
        padding: 10px;
    }
    .message {
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)
```
