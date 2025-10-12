require('dotenv').config();
const axios = require('axios');

async function testCerebrasAPI() {
    console.log('\n🧠 Testing Cerebras API...');
    console.log('🔑 API Key:', process.env.CEREBRAS_API_KEY ? 'Found ✓' : 'Not Found ✗');
    
    if (!process.env.CEREBRAS_API_KEY) {
        console.log('❌ CEREBRAS_API_KEY not configured');
        return false;
    }

    try {
        const response = await axios.post(
            'https://api.cerebras.ai/v1/chat/completions',
            {
                model: 'llama3.1-8b',
                messages: [
                    { role: 'user', content: 'Say "Hello from Cerebras!"' }
                ],
                max_tokens: 20
            },
            {
                headers: {
                    'Authorization': `Bearer ${process.env.CEREBRAS_API_KEY}`,
                    'Content-Type': 'application/json'
                },
                timeout: 10000
            }
        );

        console.log('✅ Cerebras API is WORKING!');
        console.log('📝 Response:', response.data.choices[0].message.content);
        return true;
    } catch (error) {
        console.log('❌ Cerebras API FAILED');
        if (error.response) {
            console.log('   Status:', error.response.status);
            console.log('   Error:', error.response.data?.error?.message || error.response.data);
        } else {
            console.log('   Error:', error.message);
        }
        return false;
    }
}

async function testAnthropicAPI() {
    console.log('\n🤖 Testing Anthropic API...');
    console.log('🔑 API Key:', process.env.ANTHROPIC_API_KEY ? 'Found ✓' : 'Not Found ✗');
    
    if (!process.env.ANTHROPIC_API_KEY) {
        console.log('❌ ANTHROPIC_API_KEY not configured');
        return false;
    }

    try {
        const response = await axios.post(
            'https://api.anthropic.com/v1/messages',
            {
                model: 'claude-3-sonnet-20240229',
                max_tokens: 20,
                messages: [
                    { role: 'user', content: 'Say "Hello from Claude!"' }
                ]
            },
            {
                headers: {
                    'x-api-key': process.env.ANTHROPIC_API_KEY,
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json'
                },
                timeout: 10000
            }
        );

        console.log('✅ Anthropic API is WORKING!');
        console.log('📝 Response:', response.data.content[0].text);
        return true;
    } catch (error) {
        console.log('❌ Anthropic API FAILED');
        if (error.response) {
            console.log('   Status:', error.response.status);
            console.log('   Error:', error.response.data?.error?.message || JSON.stringify(error.response.data));
        } else {
            console.log('   Error:', error.message);
        }
        return false;
    }
}

async function main() {
    console.log('═══════════════════════════════════════');
    console.log('      API KEY VALIDATION TEST');
    console.log('═══════════════════════════════════════');
    
    const cerebrasWorks = await testCerebrasAPI();
    const anthropicWorks = await testAnthropicAPI();
    
    console.log('\n═══════════════════════════════════════');
    console.log('         TEST SUMMARY');
    console.log('═══════════════════════════════════════');
    console.log('Cerebras API:', cerebrasWorks ? '✅ WORKING' : '❌ FAILED');
    console.log('Anthropic API:', anthropicWorks ? '✅ WORKING' : '❌ FAILED');
    console.log('═══════════════════════════════════════\n');
    
    if (cerebrasWorks && anthropicWorks) {
        console.log('🎉 All API keys are working! Your system is ready!');
    } else {
        console.log('⚠️  Some API keys need attention. Check the errors above.');
    }
}

main();

