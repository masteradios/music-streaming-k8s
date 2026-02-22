package com.example.auth_server.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

import com.example.auth_server.jwt.AuthEntryPointJwt;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private AuthEntryPointJwt authEntryPointJwt;

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                //.cors(cors -> cors.configurationSource(corsConfigurationSource()))
                .csrf(AbstractHttpConfigurer::disable)
                .exceptionHandling(ex -> ex.authenticationEntryPoint(authEntryPointJwt))
                .authorizeHttpRequests(authorize ->
                        authorize
                                .requestMatchers("/auth/signup", "/auth/login", "/auth/validate").permitAll()
                                .anyRequest().authenticated()
                );

        return http.build();
    }

    // @Bean
    // public CorsConfigurationSource corsConfigurationSource() {
    //     CorsConfiguration config = new CorsConfiguration();

   
    //     config.setAllowedOrigins(List.of(
    //             "http://front-end-server:5173",
    //             "http://localhost:3000"
    //     ));

    //     config.setAllowedMethods(List.of(
    //             "GET", "POST", "PUT", "DELETE", "OPTIONS"
    //     ));

    //     config.setAllowedHeaders(List.of("*"));
    //     config.setAllowCredentials(true);

    //     UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    //     source.registerCorsConfiguration("/**", config);

    //     return source;
    // }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
