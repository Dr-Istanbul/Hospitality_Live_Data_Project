import urllib.request
import urllib.error

print("Testing OpenTable access...")

try:
    # Test OpenTable with timeout
    response = urllib.request.urlopen('https://www.opentable.com/location/dallas-restaurants', timeout=10)
    content = response.read()
    print(f"✅ SUCCESS: OpenTable accessible")
    print(f"Status: {response.status}")
    print(f"Content length: {len(content)} bytes")
    
    # Check if it contains restaurant data
    if b'restaurant' in content.lower():
        print("✅ Restaurant content found")
    else:
        print("❌ No restaurant content detected")
        
except urllib.error.URLError as e:
    print(f"❌ URL Error: {e.reason}")
except Exception as e:
    print(f"❌ Error: {e}")

print("Test complete.")
