## Getting Started With Golang-jwt

ToDo 애플리케이션에 JWT 인증을 추가하기 위해 Golang-jwt 라이브러리를 사용하겠습니다. golang-jwt 패키지는 토큰 생성, 확인 및 관리와 관련된 복잡성을 추상화하는 편리한 기능 모음을 제공하여 Go 애플리케이션에서 JWT 구현을 간소화합니다.

Go 프로젝트에 Golang-jwt를 통합하려면 다음 명령을 사용하여 쉽게 설치할 수 있습니다:

```
go get -u github.com/golang-jwt/jwt/v5
```

이 명령은 필요한 의존성을 가져와서 Golang-jwt를 ToDo 애플리케이션에 쉽게 통합할 수 있도록 합니다. 이제 JWT 토큰을 만들고 사용자 정보 및 역할을 나타내는 클레임을 추가할 준비가 되었습니다.

## Creating JWT Tokens and Adding Claims

이제 JWT 인증을 추가하여 ToDo 애플리케이션을 개선해 보겠습니다. 이 섹션에서는 JWT 토큰을 만들고 사용자 정보 및 역할을 나타내는 클레임을 추가하는 데 중점을 두겠습니다.

### Step 5: Set Up Secret Key

JWT 토큰 생성을 시작하려면 먼저 필요한 패키지를 가져와서 비밀 키를 설정합니다. 비밀 키는 JWT 서명 및 확인에 모두 중요합니다. 다음은 코드입니다:

```
// Import the required packages
import (
 "fmt"
 "time"
 "net/http"
 "strconv"
 "github.com/gin-gonic/gin"
 "github.com/golang-jwt/jwt/v5"
)
// Add a new global variable for the secret key
var secretKey = []byte("your-secret-key")

// Function to create JWT tokens with claims
func createToken(username string) (string, error) {
 // ... (Code for creating JWT tokens and adding claims will go here)
}
```
