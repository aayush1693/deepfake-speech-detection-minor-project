package com.deepfake.backend.controller;

import com.deepfake.backend.service.AccountService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/manage-account")
public class AccountController {

    @Autowired
    private AccountService accountService;

    @PutMapping("/username")
    public ResponseEntity<?> changeUsername(@RequestParam String newUsername, Authentication authentication) {
        String currentUsername = authentication.getName();
        accountService.updateUsername(currentUsername, newUsername);
        return ResponseEntity.ok("Username updated successfully");
    }

    @PutMapping("/password")
    public ResponseEntity<?> changePassword(@RequestParam String newPassword, Authentication authentication) {
        String currentUsername = authentication.getName();
        accountService.updatePassword(currentUsername, newPassword);
        return ResponseEntity.ok("Password updated successfully");
    }

    @PostMapping("/profile-picture")
    public ResponseEntity<?> uploadProfilePicture(@RequestParam("file") MultipartFile file, Authentication authentication) {
        String currentUsername = authentication.getName();
        accountService.storeProfilePicture(currentUsername, file);
        return ResponseEntity.ok("Profile picture uploaded successfully");
    }
}
