-- phpMyAdmin SQL Dump
-- version 4.2.5
-- http://www.phpmyadmin.net
--
-- Host: localhost:8889
-- Generation Time: Oct 17, 2015 at 05:33 PM
-- Server version: 5.5.38
-- PHP Version: 5.5.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `articleCrawler`
--

-- --------------------------------------------------------

--
-- Table structure for table `content`
--

CREATE TABLE `content` (
`id` int(11) NOT NULL,
  `topicId` int(11) NOT NULL,
  `siteId` int(11) NOT NULL,
  `title` varchar(1000) NOT NULL,
  `body` varchar(10000) NOT NULL,
  `url` varchar(300) DEFAULT NULL
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

-- --------------------------------------------------------

--
-- Table structure for table `Sites`
--

CREATE TABLE `Sites` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `url` varchar(511) NOT NULL,
  `searchUrl` varchar(511) NOT NULL,
  `resultListing` varchar(127) NOT NULL,
  `resultUrl` varchar(127) NOT NULL,
  `absoluteUrl` varchar(127) NOT NULL,
  `pageTitle` varchar(127) NOT NULL,
  `pageBody` varchar(127) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `topics`
--

CREATE TABLE `topics` (
`id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `content`
--
ALTER TABLE `content`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Sites`
--
ALTER TABLE `Sites`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `topics`
--
ALTER TABLE `topics`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `content`
--
ALTER TABLE `content`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=28;
--
-- AUTO_INCREMENT for table `Sites`
--
ALTER TABLE `Sites`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `topics`
--
ALTER TABLE `topics`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=15;


INSERT INTO sites (name,url,searchUrl,resultListing,resultUrl,absoluteUrl,pageTitle,pageBody)

VALUES("Brookings","http://www.brookings.edu","http://www.brookings.edu/search?start=1&q=","ul.search-results li","h3.title a","FALSE","h1","div[itemprop=\"articleBody\"]"),

("Reuters","http://reuters.com","http://www.reuters.com/search/news?blob=","div.search-result-content","h3.search-result-title a","TRUE","h1","span#articleText");
