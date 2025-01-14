package com.deepfake.backend.repository;

import com.deepfake.backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.username = :newUsername WHERE u.username = :currentUsername")
    void updateUsername(String currentUsername, String newUsername);

    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.password = :newPassword WHERE u.username = :currentUsername")
    void updatePassword(String currentUsername, String newPassword);
}
