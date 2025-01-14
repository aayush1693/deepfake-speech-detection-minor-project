package com.deepfake.backend.service;

import com.deepfake.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Service
public class AccountService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public void updateUsername(String currentUsername, String newUsername) {
        userRepository.updateUsername(currentUsername, newUsername);
    }

    public void updatePassword(String currentUsername, String newPassword) {
        String encodedPassword = passwordEncoder.encode(newPassword);
        userRepository.updatePassword(currentUsername, encodedPassword);
    }

    public void storeProfilePicture(String username, MultipartFile file) {
        String directory = "profile-pictures/";
        String fileName = username + "_" + file.getOriginalFilename();
        Path path = Paths.get(directory + fileName);

        try {
            Files.createDirectories(Paths.get(directory));
            file.transferTo(new File(path.toString()));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
