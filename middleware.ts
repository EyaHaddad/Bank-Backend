import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Next.js Middleware for Frontend Security
 * 
 * Coherent with backend middleware (AdvancedSecurityMiddleware):
 * - Authentication checks for protected routes
 * - Security headers injection
 * - Route protection based on user role
 * 
 * Note: Rate limiting is handled by the backend
 */

// Public routes that don't require authentication
const PUBLIC_ROUTES = ["/", "/api"];

// Routes that require admin role
const ADMIN_ROUTES = ["/admin"];

// Routes that require client role
const CLIENT_ROUTES = ["/client"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Get auth token from cookies or check localStorage via header
  const token = request.cookies.get("access_token")?.value;
  const userRole = request.cookies.get("user_role")?.value;
  
  // Check if route is public
  const isPublicRoute = PUBLIC_ROUTES.some(
    (route) => pathname === route || pathname.startsWith("/api/")
  );
  
  // Check if accessing protected routes
  const isAdminRoute = ADMIN_ROUTES.some((route) => pathname.startsWith(route));
  const isClientRoute = CLIENT_ROUTES.some((route) => pathname.startsWith(route));
  
  // Create response with security headers (coherent with backend)
  const response = NextResponse.next();
  
  // Security Headers - matching backend AdvancedSecurityMiddleware
  // Prevent MIME type sniffing
  response.headers.set("X-Content-Type-Options", "nosniff");
  
  // Prevent clickjacking by disabling iframe embedding
  response.headers.set("X-Frame-Options", "DENY");
  
  // Enable XSS filter in browsers
  response.headers.set("X-XSS-Protection", "1; mode=block");
  
  // Referrer Policy
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  
  // Content Security Policy
  response.headers.set(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self' http://localhost:8000 https://localhost:8000;"
  );
  
  // Permissions Policy
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=()"
  );
  
  // Strict Transport Security (for production with HTTPS)
  response.headers.set(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains"
  );
  
  // Allow public routes without authentication
  if (isPublicRoute) {
    // If user is already authenticated on login page, redirect to appropriate dashboard
    if (pathname === "/" && token) {
      if (userRole === "admin") {
        return NextResponse.redirect(new URL("/admin", request.url));
      }
      return NextResponse.redirect(new URL("/client", request.url));
    }
    return response;
  }
  
  // Protected route checks
  if (!token) {
    // No token - redirect to login
    const loginUrl = new URL("/", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }
  
  // Role-based access control
  if (isAdminRoute && userRole !== "admin") {
    // Non-admin trying to access admin routes
    return NextResponse.redirect(new URL("/client", request.url));
  }
  
  if (isClientRoute && userRole === "admin") {
    // Admin trying to access client routes - allow but could redirect
    // Admins can access client routes for testing/support purposes
  }
  
  return response;
}

// Configure which routes the middleware runs on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!_next/static|_next/image|favicon.ico|public).*)",
  ],
};